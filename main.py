from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pdf2image.exceptions import (
    PDFPageCountError,
    PDFSyntaxError,
    PDFInfoNotInstalledError,
)
from pdf2image import convert_from_bytes
import pytesseract
from PIL import Image
from io import BytesIO

app = FastAPI()

@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    try:
        if file.filename.endswith(".pdf"):
            # Convert PDF to images
            pdf_bytes = await file.read()
            images = convert_from_bytes(pdf_bytes, 500)

            text = ""
            for img in images:
                text += pytesseract.image_to_string(img, lang='eng')

            return JSONResponse(content={"text": text}, status_code=200)
        else:
            raise HTTPException(status_code=422, detail="Uploaded file is not a PDF")

    except PDFPageCountError as e:
        raise HTTPException(status_code=422, detail=f"Invalid PDF: {str(e)}")
    except PDFSyntaxError as e:
        raise HTTPException(status_code=422, detail=f"Invalid PDF syntax: {str(e)}")
    except PDFInfoNotInstalledError as e:
        raise HTTPException(status_code=500, detail=f"PDFInfo not installed: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
