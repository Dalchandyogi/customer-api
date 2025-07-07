from fastapi import APIRouter, Depends, Header, status, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session, joinedload
import os

from db.database import get_db
from models.customer_details import Customer
from schemas.customer import CustomerResponse, CustomerDocsResponse

router = APIRouter()

@router.get("/get-customers")
def get_customers_by_agent(
    agent_id: int = Header(..., alias="Agent-Id"),
    db: Session = Depends(get_db),
    request: Request = None
):
    customers = (
        db.query(Customer)
        .options(
            joinedload(Customer.notes),
            joinedload(Customer.docs)
        )
        .filter(Customer.agent_id == agent_id)
        .all()
    )

    if not customers:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "statusCode": 404,
                "message": "No customers found for the given agent ID"
            }
        )

    # Build the customer list
    response_customers = []
    for customer in customers:
        customer_dict = customer.__dict__.copy()
        customer_dict['notes'] = [
            note.__dict__ for note in customer.notes
        ]
        customer_dict['docs'] = [
            CustomerDocsResponse(
                id=doc.id,
                document_type=doc.document_type,
                file_url=f"{request.url.scheme}://{request.url.netloc}/uploaded_docs/{os.path.basename(doc.file_path)}"
            ).dict() for doc in customer.docs
        ]
        response_customers.append(CustomerResponse(**customer_dict).dict())

    # Final wrapped response
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "statusCode": 200,
            "customers": response_customers
        }
    )
