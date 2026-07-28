from argparse import Namespace
from logging import getLogger
from typing import Any

import scrapy.signals as signals
from scrapy.commands.crawl import Command as ExistingCrawlCommand
from scrapy.crawler import Crawler
from scrapy.signalmanager import dispatcher

logger = getLogger(__name__)


class Command(ExistingCrawlCommand):
    def failing_exit_code_on_error(self, *args: Any, sender: Crawler, **kwargs: Any) -> None:
        if sender.stats:
            exception_count = sender.stats.get_value("downloader/exception_count")
            if exception_count:
                logger.error("At least one exception, exiting with 1")
                self.exitcode = 1
            number_items = sender.stats.get_value("item_scraped_count", 0)
            if not number_items:
                logger.error("No items scraped, exiting with 2")
                self.exitcode = 2

    def run(self, args: list[str], opts: Namespace) -> None:
        dispatcher.connect(self.failing_exit_code_on_error, signal=signals.spider_error)
        dispatcher.connect(self.failing_exit_code_on_error, signal=signals.item_error)
        dispatcher.connect(self.failing_exit_code_on_error, signal=signals.spider_closed)

        super().run(args, opts)
