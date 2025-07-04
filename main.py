from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
import secrets

from models.customer_document import CustomerDocs  
from models.customer_note import CustomerNote
from routes import add_customer, get_customers, get_one_customers, update_customer, upload_doc
from db.database import engine
from models import customer_details as model

# Create tables
model.Base.metadata.create_all(bind=engine)
CustomerNote.metadata.create_all(bind=engine)
CustomerDocs.metadata.create_all(bind=engine)

# Disable default docs and openapi
app = FastAPI(
    docs_url=None,
    redoc_url=None,
    openapi_url=None
)

# Mount static folder
app.mount("/uploaded_docs", StaticFiles(directory="uploaded_docs"), name="uploaded_docs")

# Include routers
app.include_router(add_customer.router, tags=["Customers"])
app.include_router(get_customers.router, tags=["Customers"])
app.include_router(get_one_customers.router, tags=["Customers"])
app.include_router(update_customer.router, tags=["Customers"])
app.include_router(upload_doc.router, tags=["Customers"])

# Setup Basic Auth for docs
security = HTTPBasic()

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "dalchandyogi")
    correct_password = secrets.compare_digest(credentials.password, "yogi@probus2006")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@app.get("/docs", include_in_schema=False)
def custom_swagger_ui(username: str = Depends(authenticate)):
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Secure Docs")

@app.get("/openapi.json", include_in_schema=False)
def custom_openapi(username: str = Depends(authenticate)):
    return get_openapi(
        title="Secure API",
        version="1.0.0",
        routes=app.routes
    )
