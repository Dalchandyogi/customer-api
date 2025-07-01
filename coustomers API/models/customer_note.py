from sqlalchemy import Column, Integer, String, ForeignKey
from db.database import Base

class CustomerNote(Base):
    __tablename__ = "customer_notes"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customer_details.id"))
    content = Column(String(1000), nullable=True)
    
