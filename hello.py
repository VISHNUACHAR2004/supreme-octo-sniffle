from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# GET request
@app.get("/greet")
def greet(name: str):
    return {"message": f"Hello, {name}!"}

# Define a request model for POST
class Item(BaseModel):
    name: str
    price: float
    quantity: int

# POST request
@app.post("/create-item")
def create_item(item: Item):
    total_price = item.price * item.quantity
    return {"name": item.name, "total_price": total_price}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
