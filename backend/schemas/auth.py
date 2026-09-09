from pydantic import BaseModel, ConfigDict, EmailStr, Field


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=255)

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "email": "test@test.com",
                    "password": "test1234",
                }
            ]
        }
    )


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
