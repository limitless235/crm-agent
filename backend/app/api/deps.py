from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.db import get_db
from app.models.models import User
from app.schemas.schemas import TokenPayload

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)

def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> User:
    try:
        # Verify the JWT using Supabase's HS256 JWT Secret
        # Supabase sets the audience to 'authenticated' by default in some configurations.
        payload = jwt.decode(
            token, 
            settings.SUPABASE_JWT_SECRET, 
            algorithms=["HS256"],
            options={"verify_aud": False}
        )
        
        user_id = payload.get("sub")
        email = payload.get("email")
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid token payload",
            )
    except (JWTError, Exception) as e:
        print(f"JWT Verification Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
        
    user = db.query(User).filter(User.id == user_id).first()
    
    # Auto-synchronize the user to the public.users table if they just logged in via Supabase for the first time
    if not user:
        if not email:
            raise HTTPException(status_code=400, detail="User not found and email missing from token")
        
        user = User(
            id=user_id,
            email=email,
            role="user",
            auth_provider="supabase"
        )
        db.add(user)
        try:
            db.commit()
            db.refresh(user)
        except Exception as e:
            db.rollback()
            print(f"Failed to auto-create user from verified Supabase token: {e}")
            raise HTTPException(status_code=500, detail="Failed to sync user profile")
            
    return user

def get_current_active_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.role != "admin":
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user
