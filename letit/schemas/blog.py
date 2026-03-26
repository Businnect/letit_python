from __future__ import annotations
from enum import Enum, unique
from typing import List, Optional
from pydantic import BaseModel


@unique
class BlogCategory(str, Enum):
    ANNOUNCEMENT = "ANNOUNCEMENT"


class BlogItem(BaseModel):
    body: str
    category: BlogCategory
    cover: Optional[str] = None
    is_featured: bool
    published_at: str
    slug: str
    summary: Optional[str] = None
    title: str


class BlogResponse(BaseModel):
    body: str
    category: BlogCategory
    cover: Optional[str] = None
    is_featured: bool
    published_at: str
    slug: str
    summary: Optional[str] = None
    title: str


class BlogListResponse(BaseModel):
    list: List[BlogItem]
    total_list: int
    total_pages: int
