from urllib.parse import urlparse
from typing import Optional

from pydantic import BaseModel, validator, ValidationError, HttpUrl, Field
from faker import Faker

FORBIDDEN_SLUGS = ["docs", "redoc"]
fake = Faker()


class DataModel(BaseModel):
    link: HttpUrl
    slug: Optional[str] = Field(default_factory=fake.slug)

    @validator("slug")
    def slug_is_valid(cls, v):
        if v == "":
            v = fake.slug()
        if v in FORBIDDEN_SLUGS:
            raise ValueError("Slug is forbidden")
        return v
