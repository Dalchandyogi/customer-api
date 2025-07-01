# schemas/customer.py
from typing import List, Optional
from pydantic import BaseModel, Field

class CustomerNoteCreate(BaseModel):
    content: str

class CustomerNoteResponse(BaseModel):
    id: int
    content: str

    class Config:
        orm_mode = True

# Modified schema for CustomerDocs response
class CustomerDocsResponse(BaseModel):
    id: int
    document_type: str
    file_url: str  
    class Config:
        orm_mode = True
       

class CustomerCreate(BaseModel):
    agent_id: int
    salutation: Optional[str] = None
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    gender: Optional[str] = None
    date_of_birth: Optional[str] = None
    marital_status: Optional[str] = None
    occupation: Optional[str] = None
    mobile_number: Optional[str] = None
    mobile_number_2: Optional[str] = None
    email: str
    aadhar_number: Optional[str] = None

    
    pan_number: Optional[str] = None
    gstin: Optional[str] = None
    house_or_flat_number: Optional[str] = None
    street_or_locality: Optional[str] = None
    landmark_or_area: Optional[str] = None
    pin_code: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    nominee_relation: Optional[str] = None
    nominee_name: Optional[str] = None
    nominee_gender: Optional[str] = None
    nominee_dob: Optional[str] = None

    notes: List[CustomerNoteCreate] = []


class CustomerResponse(CustomerCreate):
    id: int
    notes: List[CustomerNoteResponse] = []
    docs: List[CustomerDocsResponse] = []

    class Config:
        orm_mode = True