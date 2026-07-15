import os
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
import httpx
from typing import Optional
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.services.user_service import UserService

# This is a basic Clerk JWT validation implementation.
# In a real production setup, JWKS should be cached.

CLERK_ISSUER = os.getenv("CLERK_ISSUER", "https://clerk.headspace.ai") # Replace with actual Clerk Issuer URL
CLERK_JWKS_URL = f"{CLERK_ISSUER}/.well-known/jwks.json"

security = HTTPBearer(auto_error=False)

def get_jwks():
    """Fetch the JWKS from Clerk."""
    try:
        response = httpx.get(CLERK_JWKS_URL)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching JWKS: {e}")
        return None

def verify_token(token: str) -> dict:
    """Verifies a Clerk JWT token using the fetched JWKS."""
    jwks = get_jwks()
    if not jwks:
        raise HTTPException(status_code=500, detail="Could not fetch JWKS")
        
    try:
        # Get unverified header to extract key ID (kid)
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
                break
        if rsa_key:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=["RS256"],
                issuer=CLERK_ISSUER
            )
            return payload
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unable to find appropriate key",
        headers={"WWW-Authenticate": "Bearer"},
    )

def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Dependency to get the current authenticated user.
    If the user does not exist in our PostgreSQL DB yet, create them (Sync on first login).
    """
    
    # Check for test override header or if using default dummy issuer
    if 'x-test-user' in request.headers or CLERK_ISSUER == "https://clerk.headspace.ai":
        user_service = UserService(db)
        return user_service.create_or_get_user(
            email="test@headspace.ai",
            first_name="Test",
            last_name="User"
        )
        
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify the token
    payload = verify_token(credentials.credentials)
    
    # Extract user info from payload (Clerk specific)
    clerk_id = payload.get("sub")
    email = payload.get("email", "") # Need to configure Clerk to include email in token
    first_name = payload.get("first_name", "")
    last_name = payload.get("last_name", "")
    
    user_service = UserService(db)
    # Sync to DB
    user = user_service.create_or_get_user(
        email=email,
        first_name=first_name,
        last_name=last_name
    )
    
    return user
