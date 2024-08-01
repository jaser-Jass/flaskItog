from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from models import User, Product, Order, SessionLocal

app = FastAPI()

# Создаем модели Pydantic для запросов
class UserIn(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str

class UserOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str

    class Config:
        orm_mode = True

class OrderIn(BaseModel):
    user_id: int
    product_id: int
    order_date: str
    status: str

class OrderOut(BaseModel):
    id: int
    user_id: int
    product_id: int
    order_date: str
    status: str

    class Config:
        orm_mode = True

class ProductIn(BaseModel):
    name: str
    description: str
    price: float

class ProductOut(BaseModel):
    id: int
    name: str
    description: str
    price: float

    class Config:
        orm_mode = True

# Dependency для получения сессии
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CRUD операции для пользователей
@app.post("/users/", response_model=UserOut)
def create_user(user: UserIn, db: Session = Depends(get_db)):
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# CRUD операции для заказов
@app.post("/orders/", response_model=OrderOut)
def create_order(order: OrderIn, db: Session = Depends(get_db)):
    new_order = Order(**order.dict())
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order

@app.get("/orders/{order_id}", response_model=OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

# CRUD операции для товаров
@app.post("/products/", response_model=ProductOut)
def create_product(product: ProductIn):
    db = SessionLocal()
    new_product = Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@app.get("/products/{product_id}", response_model=ProductOut)
def get_product(product_id: int):
    db = SessionLocal()
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product