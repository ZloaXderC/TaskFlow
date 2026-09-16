from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
from uuid import uuid4,UUID
from sqlalchemy.orm import relationship



class RefreshToken:
    __tablename__ = "refresh_tokens"
