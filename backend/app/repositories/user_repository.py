from sqlalchemy.orm import Session
from app.models import models
from app.schemas import user as user_schema
from uuid import UUID

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: UUID) -> models.User:
        return self.db.query(models.User).filter(models.User.id == user_id).first()

    def get_by_email(self, email: str) -> models.User:
        return self.db.query(models.User).filter(models.User.email == email).first()

    def create(self, user: user_schema.UserCreate) -> models.User:
        db_user = models.User(
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update(self, db_user: models.User) -> models.User:
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
