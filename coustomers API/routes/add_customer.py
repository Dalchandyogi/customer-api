from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from db.database import get_db
from models import customer_details as model_customer
from models import customer_note as model_note
from schemas import customer as schema
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter()

@router.post("/add-customers/")
def create_customer(customer: schema.CustomerCreate, db: Session = Depends(get_db)):
    try:
        # Extract customer details excluding notes
        customer_data = customer.dict(exclude={'notes'})

        # Create the main customer record
        db_customer = model_customer.Customer(**customer_data)
        db.add(db_customer)
        db.commit()
        db.refresh(db_customer)

        # Handle notes separately
        for note_data in customer.notes:
            db_note = model_note.CustomerNote(customer_id=db_customer.id, **note_data.dict())
            db.add(db_note)

        db.commit() # Commit notes after adding

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "status": 201,
                "message": "Customer added successfully",
                "customer_id": db_customer.id
            }
        )
    except SQLAlchemyError as e:
        db.rollback()
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "status": 400,
                "message": "Failed to add customer",
                "details": str(e.__cause__)
            }
        )