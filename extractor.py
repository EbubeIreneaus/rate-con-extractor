import pymupdf
import pymupdf4llm
from google import genai
from model import RateConfirmation
from settings import setting
import re

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



def markdown_to_text(md: str) -> str:
    text = md

    # Remove code blocks (```...```)
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    # Remove inline code (`code`)
    text = re.sub(r"`([^`]*)`", r"\1", text)
    # Remove images ![alt](url)
    text = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"\1", text)
    # Convert links [text](url) -> text
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    # Remove headers (#, ##, ###...)
    text = re.sub(r"^#{1,6}\s*", "", text, flags=re.MULTILINE)
    # Remove bold/italic (**, __, *, _)
    text = re.sub(r"(\*\*\*|___)(.*?)\1", r"\2", text)
    text = re.sub(r"(\*\*|__)(.*?)\1", r"\2", text)
    text = re.sub(r"(\*|_)(.*?)\1", r"\2", text)
    # Remove blockquote markers
    text = re.sub(r"^>\s?", "", text, flags=re.MULTILINE)
    # Remove horizontal rules
    text = re.sub(r"^(-{3,}|\*{3,}|_{3,})$", "", text, flags=re.MULTILINE)
    # Convert table rows to spaced text, drop separator rows (|---|---|)
    text = re.sub(r"^\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)+\|?$", "", text, flags=re.MULTILINE)
    text = re.sub(r"\|", " ", text)
    # Remove list markers (-, *, +, 1.)
    text = re.sub(r"^\s*[-*+]\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*\d+\.\s+", "", text, flags=re.MULTILINE)

    # Collapse excess blank lines/whitespace
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)

    return text.strip()


def docs_extractor(bytes) -> RateConfirmation:
    try:
        docs = pymupdf.open(stream=bytes, filetype="pdf")
        content = pymupdf4llm.to_markdown(docs)
        return markdown_to_text(content)
    except Exception as e:
        print(f"Error processing document: {e}")
        return None