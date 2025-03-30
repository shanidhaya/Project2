from fastapi import FastAPI, UploadFile, File, Form
from typing import Optional
import uvicorn
import os
from questions import solve_question

app = FastAPI()

os.makedirs("file", exist_ok=True)

@app.post("/api/answers/")
async def upload_file(
    question: str = Form(...),
    file: Optional[UploadFile] = File(None)
):
    # Handle the file upload
    file_location = None
    if file:
        file_location = f"file/{file.filename}"

        # Save the file asynchronously
        with open(file_location, "wb") as f:
            content = await file.read()
            f.write(content)

        print(f"Saved File: {file_location} ({len(content)} bytes)")

    # ✅ Wait for the answer before proceeding
    result = await solve_question(question, file_location)

    # ✅ Return only the answer in JSON format
    return result


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
