from app import app
from models import db
from sqlalchemy import text

with app.app_context():
    try:
        db.session.execute(text("ALTER TABLE product ADD COLUMN stock INTEGER DEFAULT 50"))
        db.session.commit()
        print("Added stock column")
    except Exception as e:
        print("Stock column might already exist:", e)
        db.session.rollback()

    try:
        db.session.execute(text("ALTER TABLE product ADD COLUMN category VARCHAR(100) DEFAULT 'Electronics'"))
        db.session.commit()
        print("Added category column")
    except Exception as e:
        print("Category column might already exist:", e)
        db.session.rollback()
