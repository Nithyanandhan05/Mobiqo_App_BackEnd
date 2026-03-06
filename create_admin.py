from app import app
from models import db, User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def create_admin():
    with app.app_context():
        admin = User.query.filter_by(email='admin@gmail.com').first()
        if not admin:
            hashed_pw = bcrypt.generate_password_hash('admin123').decode('utf-8')
            admin = User(
                full_name='Enterprise Admin',
                email='admin@gmail.com',
                password=hashed_pw,
                is_blocked=False
            )
            db.session.add(admin)
            db.session.commit()
            print("ADMIN CREATED: admin@gmail.com / admin123")
        else:
            print("ADMIN EXISTS")

if __name__ == "__main__":
    create_admin()
