from fastapi import FastAPI, UploadFile
from extractor import docs_extractor, AI_Extractor
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import json



app = FastAPI()

app.mount('/static', StaticFiles(directory="static"), name="static")

@app.get('/', response_class=FileResponse)
async def root():
    return FileResponse('./static/index.html', media_type='text/html')

@app.post('/extract')
async def extract_content(file: UploadFile):
    if file.content_type != 'application/pdf':
        return {'success': False, "msg": "Invalid file type. Please upload a PDF file."}
    bytes = await file.read()
    content = docs_extractor(bytes)
    if not content:
         return {'success': False, "msg": "Failed to extract content from the document."}       
    ai_res = AI_Extractor(content)
    if not ai_res['success']:
        return {'success': False, "msg": ai_res['msg']}
    return {'success': True, "data": ai_res['data']}