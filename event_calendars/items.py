# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html


from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

from uuid import UUID, uuid5
ns = UUID('b44256d5-dee8-4dee-9fd9-31451e47984e')


def current_datetime() -> datetime:
    return datetime.now(tz=timezone.utc)

@dataclass
class Event():
    summary: str

    start_datetime: datetime | None
    end_datetime: datetime | None

    url: Optional[str]
    location: Optional[str]

    original_description: str = ""

    updated_at: datetime = field(default_factory=current_datetime)

    @property
    def description(self) -> str:
        assembled: str = self.original_description
        if self.url:
            assembled += f"\nURL: {self.url}"
        return assembled

    @property
    def uid(self) -> str:
        return str(uuid5(ns, str(self.url)))

    def __repr__(self) -> str:
        return f"{self.start_datetime}: {self.url}: {self.summary}"


@dataclass
class BookableEvent(Event):
    facility: Optional[str] = None
    price_range: Optional[str] = None
    spots_remaining: Optional[str] = None
    category: Optional[str] = None

    @property
    def rendered_description(self) -> str:
        assembled: str = self.original_description
        if self.url:
            assembled += f"\nURL: {self.url}"
        if self.facility:
            assembled += f"\nFacility: {self.facility}"
        if self.price_range:
            assembled += f"\nPrice: {self.price_range}"
        if self.spots_remaining:
            assembled += f"\nSpace: {self.spots_remaining}"
        if self.category:
            assembled += f"\nCategory: {self.category}"
        return assembled
