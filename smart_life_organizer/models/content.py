from datetime import datetime
from typing import TYPE_CHECKING, List, Optional, Union

from pydantic import BaseModel, Extra
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from smart_life_organizer.security import User


class Content(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    slug: Optional[str] = Field(default=None)
    text: str
    published: bool = False
    created_time: str = Field(default_factory=lambda: datetime.now().isoformat())
    tags: str = Field(default="")
    user_id: Optional[int] = Field(foreign_key="user.id")

    user: Optional["User"] = Relationship(back_populates="contents")


class ContentResponse(BaseModel):
    id: int
    title: str
    slug: Optional[str]
    text: str
    published: bool
    created_time: str
    tags: List[str]
    user_id: int

    def __init__(self, *args, **kwargs):
        tags = kwargs.pop("tags", None)
        if tags and isinstance(tags, str):
            kwargs["tags"] = tags.split(",")
        super().__init__(*args, **kwargs)


class ContentIncoming(BaseModel):
    title: Optional[str]
    text: Optional[str]
    published: Optional[bool] = False
    tags: Optional[Union[List[str], str]]
    slug: Optional[str] = None

    class Config:
        extra = Extra.allow
        arbitrary_types_allowed = True

    def __init__(self, *args, **kwargs):
        tags = kwargs.pop("tags", None)
        if tags and isinstance(tags, list):
            kwargs["tags"] = ",".join(tags)
        super().__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        if self.title:
            self.slug = self.title.lower().replace(" ", "-")