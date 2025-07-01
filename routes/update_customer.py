from fastapi import APIRouter, Depends, status, HTTPException, Header
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session, joinedload 
from db.database import get_db
from models import customer_details as model_customer
from models import customer_note as model_note
from schemas import customer as schema
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter()

@router.put("/update-customer", response_model=schema.CustomerResponse)
def update_customer(
    customer_update: schema.CustomerCreate, # Use CustomerCreate without documents
    customer_id: int = Header(..., alias="Customer-Id"),
    db: Session = Depends(get_db)
):
    db_customer = db.query(model_customer.Customer).filter(model_customer.Customer.id == customer_id).first()
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    try:
        # Update main customer fields
        for field, value in customer_update.dict(exclude={'notes'}).items(): 
            setattr(db_customer, field, value)

        # Update notes
        if customer_update.notes is not None:
            db.query(model_note.CustomerNote).filter(model_note.CustomerNote.customer_id == customer_id).delete()
            for note_data in customer_update.notes:
                db_note = model_note.CustomerNote(customer_id=customer_id, **note_data.dict())
                db.add(db_note)
        
        db.commit()
        db.refresh(db_customer)

        db_customer = db.query(model_customer.Customer).options(
            joinedload(model_customer.Customer.notes),
            joinedload(model_customer.Customer.docs)
        ).filter(model_customer.Customer.id == customer_id).first()

        return db_customer

    except SQLAlchemyError as e:
        db.rollback()
        return JSONResponse(
            status_code=400,
            content={
                "status": "400",
                "error": f"Failed to update customer: {str(e.__cause__)}"
            }
        )