from datetime import datetime, timezone

from sqlalchemy import ForeignKey,DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
from uuid import uuid4,UUID
from sqlalchemy.orm import relationship



class RefreshTokenORM(Base):
    __tablename__ = "refresh_tokens"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    jti: Mapped[UUID] = mapped_column(nullable=False, unique=True)
    expires_at:Mapped[datetime] = mapped_column(DateTime(timezone=True),nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),nullable=False, default=lambda:datetime.now(timezone.utc))
    revoked: Mapped[bool] = mapped_column(nullable=False, default=False)
    user = relationship("UserORM", back_populates="refresh_tokens")