# routes/get_one_customers.py
from fastapi import APIRouter, Depends, Header, status, Request 
from fastapi.params import Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session, joinedload
import os

from db.database import get_db
from models.customer_details import Customer
from schemas.customer import CustomerResponse, CustomerDocsResponse

router = APIRouter()

@router.get("/get-one-customer", response_model=CustomerResponse)
def get_customer_by_id(
    request: Request,
    customer_id: int = Query(..., alias="customer_id"), 
    db: Session = Depends(get_db)
):
    customer = db.query(Customer).options(
        joinedload(Customer.notes),
        joinedload(Customer.docs)
    ).filter(
        Customer.id == customer_id
    ).first()

    if not customer:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "statusCode": 404,
                "message": "Customer not found for the given ID"
            }
        )

    # Manually map to CustomerResponse to generate file_url
    customer_dict = customer.__dict__.copy()
    customer_dict['notes'] = [
        note.__dict__ for note in customer.notes
    ]
    customer_dict['docs'] = [
        CustomerDocsResponse(
            id=doc.id,
            document_type=doc.document_type,
            file_url=f"{request.url.scheme}://{request.url.netloc}/uploaded_docs/{os.path.basename(doc.file_path)}"
        ) for doc in customer.docs
    ]

    return CustomerResponse(**customer_dict)
