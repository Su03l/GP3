from fastapi import FastAPI
from smart_life_organizer.db import engine
from smart_life_organizer.models.user import Base
from smart_life_organizer.routes import main_router  # تأكد أنك رابط الراوترات

# ✅ لازم تعرّف app قبل استخدامه
app = FastAPI()

@app.on_event("startup")
def on_startup():
    print("✅ Server starting...")
    Base.metadata.create_all(bind=engine)

# ✅ ربط الراوترات
app.include_router(main_router)

@app.get("/")
def root():
    return {"message": "Server is running ✅"}
