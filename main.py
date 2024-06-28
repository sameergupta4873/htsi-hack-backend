from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import requests
import shutil
import google.generativeai as genai
import os

API_KEY = "AIzaSyAzKZUUI-fD--F1Yfo02AlRQc-LiVeRkQQ"

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')

app = FastAPI()

origins = [
    # "http://localhost",
    # "http://localhost:8000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],
)
custom_prompt = ''' 
check if this image is a tool and that of company HILTI,
if yes:
    - give a json object with three parameters (tool_details, tool_usage_steps, youtube_links)
    - here tool_details is the details of the tool in the image, 
    - tool_usage_steps is stepwise usage of the tool,
    - youtube_links is an array of links of youtube tutorials of the tool make sure it is available on youtube
    if there is no links return empty array.
if no:
    - give a json with error message that the image is not of a hilti tool.
'''

@app.post("/send_to_gemini")
async def send_to_gemini(file: UploadFile = File(...), text: str = Form(...)):
    file_location = f"./{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    sample_file = genai.upload_file(path=file_location, display_name=file.filename)
    print(f"Uploaded file '{sample_file.display_name}' as: {sample_file.uri}")

    response = model.generate_content([sample_file, custom_prompt])
    print(f"Generated content: {response.text}")
    return {"content": response.text}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="192.168.95.150", port=8000)
