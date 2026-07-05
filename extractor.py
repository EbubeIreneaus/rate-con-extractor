import pymupdf4llm
import pymupdf
import pymupdf_layout
from google import genai
from model import RateConfirmation
from settings import setting

def AI_Extractor(content):
    try:
        client = genai.Client(api_key=setting.GEMINI_API_KEY)
        interaction = client.interactions.create(
            model="gemini-3.5-flash",
            input=f"""
    You are an AI assistant that extracts structured data from rate confirmation documents.
    The document content is provided below in text format. Your task is to extract the 
    relevant information and return it in a structured JSON format that matches the 
    RateConfirmation model. If any information is missing, please return None for that field.
    Ensure that the JSON output is valid and adheres to the schema defined in the 
    RateConfirmation model. The output should be a single JSON object without any additional 
    text or explanations. Here is the document content:

    {content}
    """,
            response_format={
                "type": "text",
                "mime_type": "application/json",
                "schema": RateConfirmation.model_json_schema()
            }
        )

        text =  interaction.output_text
        if text.startswith('```json'):
            text = text[len('```json'):].strip()
        if text.endswith('```'):
            text = text[:-len('```')].strip()
        response = RateConfirmation.model_validate_json(text)
        return {"success": True, "data": response}
    except Exception as e:
        print(f"Error in AI extraction: {e}")
        return {"success": False, "msg": f"Error in AI extraction: {e}" }


def docs_extractor(bytes) -> RateConfirmation:
    try:
        docs = pymupdf.open(stream=bytes, filetype="pdf")
        content = pymupdf4llm.to_text(docs)
        return content
    except Exception as e:
        print(f"Error processing document: {e}")
        return None