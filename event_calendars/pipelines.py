import re
from typing import Self

from scrapy import Spider
from scrapy.crawler import Crawler
from scrapy.exceptions import DropItem

from .items import BookableEvent, Event
from .spiders.ymca_burlington import YmcaBurlington
from .spiders.ymca_burlington_hamilton import YmcaHamiltonBurlingtonPools
from .spiders.ymca_hamilton import YmcaHamilton

reject_names = [
    "Adult Swim Lesson",
    "Karate",
    "Back to Living Well",
    "Badminton",
    "Balance Plus",
    "Barre",  # A ballet-inspired group fitness class
    "Basketball",
    "Birthday Party",  # private
    "Child Minding",
    "Endurance Cycle",
    "Dodgeball",
    "Hockey",
    "Dance",
    "HIIT",  # Maybe
    "Pickleball",
    "Soccer",
    "Strong Nation",
    "Volleyball",
    "TRX",  # suspension
    "Queenax",  # functional training system
    "Open Gym",  # fills all remaining space
    "WalkFit",  # A gentle low impact class using Activator walking poles
]

reject_categories = [
    "Birthday Party",
    "Healthy Hearts",
    "YThrive",
]

age_range_years_regex = re.compile(r"\((\d+) ?- ?(\d+)(yrs)?\)")


class DropUninterestingYmcaEvents:
    spider_class: type[Spider]
    spider: Spider | None

    def __init__(self, crawler: Crawler):
        self.spider_class = crawler.spidercls
        self.spider = crawler.spider

    @classmethod
    def from_crawler(cls, crawler: Crawler) -> Self:
        return cls(crawler)

    def process_item(self, item: Event) -> Event:
        if not isinstance(self.spider, (YmcaBurlington, YmcaHamilton)):
            return item

        if not isinstance(item, BookableEvent):
            return item

        # this item is from a YMCA spider.
        assert isinstance(self.spider, YmcaHamiltonBurlingtonPools)

        if item.category in reject_categories:
            raise DropItem(f"YMCA filter dropping {item.summary=} from category {item.category}")

        for n in reject_names:
            if n in item.summary:
                raise DropItem(f"YMCA filter dropping {item.summary=} for name {n}")

        for check_field in (item.category, item.summary, item.description):
            if check_field is None:
                continue
            if "(infant-36 months)" in check_field:
                raise DropItem("Limited to infant-36 months")

            m = age_range_years_regex.search(check_field)
            if m:
                low = int(m.group(1))
                high = int(m.group(2))
                if not (low < 40 < high):
                    raise DropItem(f"Limited to age range {low}-{high}")

        return item
