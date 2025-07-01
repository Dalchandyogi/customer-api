from sqlalchemy import Column, Integer, String
from db.database import Base
from sqlalchemy.orm import relationship

class Customer(Base):
    __tablename__ = 'customer_details'

    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer,nullable=True)

    # Personal Information
    salutation = Column(String(10), nullable=True)
    first_name = Column(String(50), nullable=False)
    middle_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=False)
    gender = Column(String(10), nullable=True)
    date_of_birth = Column(String(20), nullable=True) 
    marital_status = Column(String(20), nullable=True)  
    occupation = Column(String(50), nullable=True)

    # Contact and Other Details
    mobile_number = Column(String(15), nullable=True)
    mobile_number_2 = Column(String(15), nullable=True)
    email = Column(String(100), unique=True, nullable=False)
    aadhar_number = Column(String(20), unique=True, nullable=True)
    pan_number = Column(String(10), unique=True, nullable=True)
    gstin = Column(String(15), unique=True, nullable=True)

    # Address Details
    house_or_flat_number = Column(String(20), nullable=True)
    street_or_locality = Column(String(100), nullable=True)
    landmark_or_area = Column(String(100), nullable=True)
    pin_code = Column(String(10), nullable=True)
    state = Column(String(50), nullable=True)
    city = Column(String(50), nullable=True)

    # Nomine Details
    nominee_relation = Column(String(100), nullable=True)
    nominee_name = Column(String(100), nullable=True)
    nominee_gender = Column(String(10), nullable=True)
    nominee_dob = Column(String(20), nullable=True)

    notes = relationship(
        "CustomerNote",
        backref="customer",
        cascade="all, delete-orphan",
        lazy="joined"
    )

    docs = relationship(
        "CustomerDocs",
        backref="customer",
        cascade="all, delete-orphan",
        lazy="joined"
    )
