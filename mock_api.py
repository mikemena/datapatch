from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class ProviderCategory(BaseModel):
    providerId: str
    fbNumber: str
    categoryCode: str
    newCategoryCode: str

@app.post("/api/provider_category")
async def create_provider(provider: ProviderCategory):
    # Simulate API processing
    return {
        "status": "success",
        "data": provider.dict(),
        "message": "Provider category created successfully"
    }

@app.get("/api/products/{product_id}")
async def get_product(product_id: str):
    return {
        "status": "success",
        "data": {"id": product_id, "name": "Test Product"}
    }

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)