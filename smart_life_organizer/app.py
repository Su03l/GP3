import io
import os
import logging
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .config import settings
from .db import create_db_and_tables, engine
from .routes import main_router

# إعدادات اللوق
logging.basicConfig(level=logging.DEBUG)

# دالة قراءة الملفات (مثلاً لقراءة VERSION)
def read(*paths, **kwargs):
    content = ""
    with io.open(
        os.path.join(os.path.dirname(__file__), *paths),
        encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content

# وصف API
description = """
smart_life_organizer API helps you do awesome stuff. 🚀
"""

# إنشاء تطبيق FastAPI
app = FastAPI(
    title="smart_life_organizer",
    description=description,
    version="0.1.0",  # ← هنا تم التصحيح (string بدلاً من float)

    terms_of_service="http://smart_life_organizer.com/terms/",
    contact={
        "name": "author_name",
        "url": "http://smart_life_organizer.com/contact/",
        "email": "author_name@smart_life_organizer.com",
    },
    license_info={
        "name": "The Unlicense",
        "url": "https://unlicense.org",
    },
)

# إعدادات CORS
if settings.server and settings.server.get("cors_origins", None):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.server.cors_origins,
        allow_credentials=settings.get("server.cors_allow_credentials", True),
        allow_methods=settings.get("server.cors_allow_methods", ["*"]),
        allow_headers=settings.get("server.cors_allow_headers", ["*"]),
    )

# ربط الراوترات
app.include_router(main_router)

# تجهيز قاعدة البيانات عند تشغيل التطبيق
@app.on_event("startup")
def on_startup():
    print("✅ Server is starting...")
    create_db_and_tables(engine)
