from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
from uuid import uuid4,UUID
from sqlalchemy.orm import relationship

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.user import TaskORM


class UserORM(Base):
    __tablename__ = 'users'

    id: Mapped[UUID] = mapped_column(primary_key=True,default=uuid4)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str] = mapped_column()
    tasks: Mapped[list["TaskORM"]] = relationship(back_populates="user", cascade="all, delete-orphan") # type: ignore
    refresh_tokens = relationship("RefreshTokenORM", back_populates = "user")



