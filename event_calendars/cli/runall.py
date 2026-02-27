import argparse
from argparse import Namespace
from logging import getLogger

from scrapy.commands import ScrapyCommand
from scrapy.crawler import AsyncCrawlerProcess
from scrapy.exceptions import UsageError
from scrapy.settings import Settings
from scrapy.spiderloader import get_spider_loader
from scrapy.utils.project import get_project_settings

logger = getLogger(__name__)


class RunAll(ScrapyCommand):
    def add_options(self, parser: argparse.ArgumentParser) -> None:
        super().add_options(parser)
        parser.add_argument(
            "--except",
            dest="except_spider",
            action="append",
            default=[],
            metavar="SPIDER",
            help="do not run named spider (may be repeated)",
        )

    def short_desc(self) -> str:
        return "Run all non-merge spiders"

    def run(self, args: list[str], opts: Namespace) -> None:
        assert self.settings is not None
        assert isinstance(self.crawler_process, AsyncCrawlerProcess)
        self.exitcode = run_all(args, self.settings, self.crawler_process)


def run_all(args: list[str], settings: Settings | None, crawler_process: AsyncCrawlerProcess | None) -> int:
    if len(args) != 0:
        raise UsageError("Passing arguments to 'scrapy runall' is not supported")
    if settings is None:
        settings = get_project_settings()
    if crawler_process is None:
        crawler_process = AsyncCrawlerProcess(settings)

    spider_loader = get_spider_loader(settings)

    all_spiders = sorted(spider_loader.list())
    logger.info(f"Loading spiders: {all_spiders}")
    for spider_name in all_spiders:
        spider_info = spider_loader.load(spider_name)
        if getattr(spider_info, "skip_in_runall", False):
            print(f"Skip {spider_name=} - skip_in_runall set")
        else:
            print(f"Starting {spider_name=}")
            crawler_process.crawl(spider_name)

    crawler_process.start()  # the script will block here until all crawling jobs are finished
    if crawler_process.bootstrap_failed:
        return 1

    return 0
