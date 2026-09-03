from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, field_validator



class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)

    
    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str):
        if not value.strip():
            raise ValueError("Title cannot be empty")
        
        return value.strip()

class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    title: str
    complited: bool

class TaskUpdate(BaseModel):
    title: str | None = None
    complited: bool | None = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value:str|None):
        if value is None:
            return value
        
        if not value.strip():
            raise ValueError("Title cannot be empty")

        return value.strip()
            