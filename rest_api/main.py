from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from functions.queries import display_products, display_orders
from functions.auth import get_current_active_user, generate_access_token, Token, User


app = FastAPI()


# Route for generating access token
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    dct = generate_access_token(form_data)
    return dct


# Route to retrieve all orders
@app.get("/orders/")
def get_orders(current_user: User = Depends(get_current_active_user)):
    data = display_orders()
    return data


# Route to retrieve products by category
@app.get("/{category}/")
def get_products(category, current_user: User = Depends(get_current_active_user)):
    categories = ["boots", "balls"]
    if category not in categories:
        raise HTTPException(status_code=404, detail="Category not found")

    data = display_products(category)
    return data
