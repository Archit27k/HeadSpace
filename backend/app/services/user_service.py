from app.repositories.user_repository import UserRepository
from app.schemas import user as user_schema
from app.models.models import User
from sqlalchemy.orm import Session
from uuid import UUID

class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def get_user(self, user_id: UUID) -> User:
        return self.repo.get_by_id(user_id)

    def get_user_by_email(self, email: str) -> User:
        return self.repo.get_by_email(email)

    def create_or_get_user(self, email: str, first_name: str, last_name: str) -> User:
        existing_user = self.get_user_by_email(email)
        if existing_user:
            return existing_user
        
        user_create = user_schema.UserCreate(
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        return self.repo.create(user_create)
