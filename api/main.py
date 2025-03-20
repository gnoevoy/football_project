from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pathlib import Path
import sys


PROJECT_DIR = Path(__file__).parent.parent
sys.path.append(str(PROJECT_DIR))


from api.helper_functions import get_db, display_products, display_orders
from api.auth import get_current_active_user, generate_access_token
from api.auth import Token, User


app = FastAPI()


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    dct = generate_access_token(form_data.username, form_data.password)
    return dct


@app.get("/{category}/", response_model=User)
def get_products(category, db=Depends(get_db), current_user: User = Depends(get_current_active_user)):
    categories = ["boots", "balls", "orders"]
    if category not in categories:
        raise HTTPException(status_code=404, detail="Category not found")

    if category == "orders":
        data = display_orders(db)
    else:
        data = display_products(db, category)

    return data
