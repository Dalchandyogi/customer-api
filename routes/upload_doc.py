from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, Request 
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from models import customer_document
from db.database import get_db
import os
import shutil

router = APIRouter()

UPLOAD_DIR = "uploaded_docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_upload_file(upload_file, destination):
    with open(destination, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)

@router.post("/upload_doc/")
async def upload_customer_doc(
    customer_id: int = Form(...),
    document_type: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    request: Request = Request 
):
    # Check if customer exists
    from models.customer_details import Customer
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        return JSONResponse(
            status_code=404,
            content={
                "status": 404,
                "error": "The given customer ID is not found. Please Provide right customer ID."
            }
        )
    if file.content_type not in ["image/jpeg", "image/png"]:
        return JSONResponse(
            status_code=400,
            content={
                "status": 400,
                "error": "Invalid file type. Only JPEG and PNG images are allowed."
            }
        )
    image_data = await file.read()

    
    file_ext = os.path.splitext(file.filename)[1]
    
    file_name = f"customer_{customer_id}_doc_{os.urandom(8).hex()}{file_ext}" 
    file_path_on_server = os.path.join(UPLOAD_DIR, file_name)

    try:
        with open(file_path_on_server, "wb") as buffer:
            buffer.write(image_data) 

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not save file locally: {e}")

    
    file_public_url = f"{request.url.scheme}://{request.url.netloc}/uploaded_docs/{file_name}"

    new_doc = customer_document.CustomerDocs(
        customer_id=customer_id,
        document_type=document_type,
        image=image_data, 
        file_path=file_path_on_server 
    )

    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)

    return {
        "status": 200,
        "message": "Document uploaded successfully",
        "doc_id": new_doc.id,
        "customer_id": new_doc.customer_id,
        "document_type": new_doc.document_type,
        "file_url": file_public_url 
    }
