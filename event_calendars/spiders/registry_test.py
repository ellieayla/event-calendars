from . import registry

from scrapy import Spider
from unittest import mock


def test_registry() -> None:
    with mock.patch("event_calendars.spiders.registry._spiders", new_callable=list):

        @registry.register
        class MySpider(Spider):
            ...

        spider_list = registry.get()
        assert len(spider_list) == 1
        only_item = spider_list[0]

        assert only_item is MySpider


def test_registry_configured() -> None:

    spider_list = registry.get()
    assert len(spider_list) > 1
