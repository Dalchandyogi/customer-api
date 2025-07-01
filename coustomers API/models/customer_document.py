from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.mysql import LONGBLOB
from db.database import Base


class CustomerDocs(Base):
    __tablename__ = "customer_docs"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customer_details.id"))
    document_type = Column(String(100))
    image = Column(LONGBLOB, nullable=False)
    file_path = Column(String(500), nullable=True) 