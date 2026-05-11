from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.database import Base, engine, SessionLocal
from app import models, schemas
from app.security import hash_password, verify, create_token
from app.logging import log
import subprocess
import joblib
from app.ml.feature_extractor import extract_features
import json
from datetime import datetime
from fastapi import Request

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- REGISTER ----------------
@app.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(
        username=user.username,
        password=hash_password(user.password)
    )
    db.add(db_user)
    db.commit()
    return {"message": "registered"}

# ---------------- LOGIN ----------------
@app.post("/login")
def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter_by(username=user.username).first()

    if not db_user or not verify(user.password, db_user.password):
        raise HTTPException(401)

    return {"token": create_token(user.username)}

# ---------------- PRODUCTS CRUD ----------------
@app.post("/products")
def create_product(p: schemas.ProductCreate, db: Session = Depends(get_db)):
    prod = models.Product(**p.dict())
    db.add(prod)
    db.commit()
    return {"message": "created"}

@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()

@app.put("/products/{id}")
def update_product(id: int, p: schemas.ProductCreate, db: Session = Depends(get_db)):
    prod = db.query(models.Product).get(id)
    if not prod:
        raise HTTPException(404)
    prod.name = p.name
    prod.price = p.price
    db.commit()
    return {"message": "updated"}

@app.delete("/products/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    prod = db.query(models.Product).get(id)
    if not prod:
        raise HTTPException(404)
    db.delete(prod)
    db.commit()
    return {"message": "deleted"}

# ---------------- ORDERS ----------------
@app.post("/orders")
def order(o: schemas.OrderCreate, db: Session = Depends(get_db)):
    db_order = models.Order(**o.dict())
    db.add(db_order)
    db.commit()
    return {"message": "order placed"}

# ---------------- THREAT DETECTION ----------------
model = joblib.load("app/ml/model.pkl")

@app.get("/threat-report")
def threat_report():
    features_dict = extract_features("logs/app.log")

    results = {}

    for ip, stats in features_dict.items():
        X = [[
            stats["repeated_401"],
            stats["total_requests"],
            stats["unknown_paths"]
        ]]

        prediction = model.predict(X)[0]

        results[ip] = "suspicious" if prediction == 1 else "normal"

    return results


@app.middleware("http")
async def log_requests(request: Request, call_next):
    response = await call_next(request)

    log_entry = {   
        "time": str(datetime.utcnow()),
        "method": request.method,
        "path": request.url.path,
        "status": response.status_code,
        "ip": request.client.host
    }

    with open("logs/app.log", "a") as f:
        f.write(json.dumps(log_entry) + "\n")

    return response