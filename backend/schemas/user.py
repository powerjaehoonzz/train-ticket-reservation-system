from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, EmailStr

from enums.user import UserRole


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=255)
    name: str = Field(min_length=1, max_length=50)

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "email": "test@test.com",
                    "password": "test1234",
                    "name": "테스트",
                }
            ]
        }
    )


class UserRead(BaseModel):
    id: int
    email: str
    name: str
    role: UserRole
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
