from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
from uuid import uuid4,UUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.user import UserORM


class TaskORM(Base):
    __tablename__ = "Tasks"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column()
    complited: Mapped[bool] = mapped_column(default=False)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    user: Mapped["UserORM"] = relationship(back_populates="tasks")