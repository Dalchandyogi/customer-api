# main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from models.customer_document import CustomerDocs # Import CustomerDocs
from models.customer_note import CustomerNote
from routes import add_customer
from routes import get_customers
from routes import get_one_customers, update_customer, upload_doc
from db.database import engine
from models import customer_details as model

model.Base.metadata.create_all(bind=engine)
CustomerNote.metadata.create_all(bind=engine)
CustomerDocs.metadata.create_all(bind=engine) # Ensure CustomerDocs table is created


app = FastAPI()
app.mount("/uploaded_docs", StaticFiles(directory="uploaded_docs"), name="uploaded_docs")

app.include_router(add_customer.router, tags=["Customers"])
app.include_router(get_customers.router, tags=["Customers"])
app.include_router(get_one_customers.router, tags=["Customers"])
app.include_router(update_customer.router, tags=["Customers"])
app.include_router(upload_doc.router, tags=["Customers"])