from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from helpers.db_queries import get_db, display_products, display_orders
from helpers.auth import get_current_active_user, generate_access_token
from helpers.auth import Token, User

app = FastAPI()


# Route for generating access token
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    dct = generate_access_token(form_data)
    return dct


# Route to retrieve all orders
@app.get("/orders/", response_model=User)
def get_orders(db=Depends(get_db), curent_user: User = Depends(get_current_active_user)):
    data = display_orders(db)
    return data


# Route to retrieve products by category
@app.get("/{category}/", response_model=User)
def get_products(category, db=Depends(get_db), current_user: User = Depends(get_current_active_user)):
    categories = ["boots", "balls"]
    if category not in categories:
        raise HTTPException(status_code=404, detail="Category not found")

    data = display_products(db, category)
    return data
