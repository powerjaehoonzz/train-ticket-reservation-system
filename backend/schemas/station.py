from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from enums.station import Region


class StationCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    code: str = Field(min_length=1, max_length=5)
    city: str = Field(min_length=1, max_length=50)
    region: Region

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "name": "서울역",
                    "code": "SEO",
                    "city": "서울",
                    "region": "수도권",
                }
            ]
        }
    )


class StationRead(BaseModel):
    id: int
    name: str
    code: str
    city: str
    region: Region
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
