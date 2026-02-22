from sqlalchemy.orm import Session
from app.models.models import User
from app.schemas.schemas import UserCreate
from app.core.security import get_password_hash, verify_password

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, obj_in: UserCreate):
    hashed_pw = get_password_hash(obj_in.password) if obj_in.password else None
    db_obj = User(
        email=obj_in.email,
        hashed_password=hashed_pw,
        role=obj_in.role,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not user.hashed_password:
        return None  # OAuth-only user, can't login with password
    if not verify_password(password, user.hashed_password):
        return None
    return user

def get_or_create_google_user(db: Session, email: str, google_sub: str):
    """Find existing user or create a new one for Google OAuth."""
    user = get_user_by_email(db, email)
    if user:
        # Link Google to existing local account if not already linked
        if not user.auth_provider_id:
            user.auth_provider_id = google_sub
            if user.auth_provider == "local":
                user.auth_provider = "local+google"
            db.commit()
            db.refresh(user)
        return user

    # Create new Google-authenticated user
    db_obj = User(
        email=email,
        hashed_password=None,
        role="user",
        auth_provider="google",
        auth_provider_id=google_sub,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
