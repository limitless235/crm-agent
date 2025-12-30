import uuid
from app.core.db import SessionLocal
from app.models.models import User
from app.core.security import get_password_hash

def create_admin():
    db = SessionLocal()
    try:
        email = "admin@antigravity.internal"
        # Check if exists
        user = db.query(User).filter(User.email == email).first()
        if user:
            print(f"User {email} already exists.")
            return

        admin_user = User(
            id=uuid.uuid4(),
            email=email,
            hashed_password=get_password_hash("admin123"),
            role="admin"
        )
        db.add(admin_user)
        db.commit()
        print(f"Admin user created successfully: {email}")
    except Exception as e:
        print(f"Error creating admin: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()
