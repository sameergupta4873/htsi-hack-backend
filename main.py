from fastapi import FastAPI, File, UploadFile, Form
import requests
import shutil
import google.generativeai as genai
import os

API_KEY = "AIzaSyAzKZUUI-fD--F1Yfo02AlRQc-LiVeRkQQ"

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')

app = FastAPI()

@app.post("/send_to_gemini")
async def send_to_gemini(file: UploadFile = File(...), text: str = Form(...)):
    file_location = f"./{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    sample_file = genai.upload_file(path=file_location, display_name=file.filename)
    print(f"Uploaded file '{sample_file.display_name}' as: {sample_file.uri}")

    response = model.generate_content([sample_file, text])
    print(f"Generated content: {response.text}")
    return {"content": response.text}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
