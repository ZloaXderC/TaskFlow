import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
from uuid import uuid4,UUID
from sqlalchemy.orm import relationship



class RefreshTokenORM(Base):
    __tablename__ = "refresh_tokens"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    jti: Mapped[UUID] = mapped_column(nullable=False, unique=True)
    expires_at:Mapped[datetime] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.datetime.utcnow)
    revoked: Mapped[bool] = mapped_column(nullable=False, default=False)
    user = relationship("User", back_populates="refresh_tokens")