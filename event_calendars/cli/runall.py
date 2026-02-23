

"""
# Existing things to support:
communitybikeways
ymcahbb-pools
burlington-pools
burlington-events

# Wayback feature needed:
cycleto.ca (via wayback)

# Future work
https://www.newhopecommunitybikes.com/womens-programming

https://www.facebook.com/groups/respectcyclists/events
- note leaked fb_access_token: https://data.accentapi.com/feed/6489.json?nocache=1770998802334
    = {"group_id":"562446623836569"}
    https://www.facebook.com/events/789092220770764
    https://rss.app/api/widget/feed/742NrVIIE5uioVmF?isPreview=1&isIframe=1

{
  "group_details": {
    "id": "562446623836569",
    "name": "Advocacy for Respect for Cyclists",
    "url": "http://facebook.com/groups/respectcyclists",
    "description": "ARC website:     www.respectcyclists.org\n\nARC on Twitter:  https://twitter.com/RespectTO\n\nARC Ghost BIke GTA Map:  https://www.arcgis.com/apps/dashboards/b59296db08bc4e6cb583aae7c5288b66\n\nARC is a cycling advocacy group formed in 1996 after the arrest of two cyclists at Critical Mass and the death of cyclist Erin Krauser.\n\nARC's chief role is the organizing of cyclist memorials and the placing of Ghost bikes.\n\nWe welcome all cyclists regardless of economic or membership status. We don't care who you are, if you are a cyclist we will help you.",
    "group_location": {
      "name": "Toronto, Ontario",
      "id": "110941395597405"
    },
    "privacy": "Public group",
    "has_questions": false,
    "cover_photo": {
      "uri": "https://scontent-cgk1-2.xx.fbcdn.net/v/t39.30808-6/447836681_10163590193479046_4282936966233871889_n.jpg?stp=dst-jpg_p480x480_tt6&_nc_cat=108&ccb=1-7&_nc_sid=25d718&_nc_ohc=0u6dmoZGZ8oQ7kNvwHxU-x6&_nc_oc=AdmgS1aFDhdSkXpiiBUoyeCTBJnjdAALoeYrYPFwBZO116-MpmKb_NqzNOk0OSNdbRU&_nc_zt=23&_nc_ht=scontent-cgk1-2.xx&_nc_gid=6Q5AE6FkYQWkv5Gcbkyi2Q&oh=00_AfunJQ_w6asdyFdD7OQCUiuY9wJ0_hk9G63Y2X7nZTYDuA&oe=699E7BA9",
      "width": 698,
      "height": 480
    },
    "members_count": 2800
  }
}
"""

#from . import spiders  # pyright: ignore[reportUnusedImport]
from argparse import Namespace

from scrapy.commands import ScrapyCommand

#from .spiders.registry import get

import argparse
from scrapy.settings import Settings
from scrapy.crawler import AsyncCrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.spiderloader import get_spider_loader
from scrapy.exceptions import UsageError


from logging import getLogger
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

    for spider_name in sorted(spider_loader.list()):
        crawler_process.crawl(spider_name)

    crawler_process.start()  # the script will block here until all crawling jobs are finished
    if crawler_process.bootstrap_failed:
        return 1

    return 0
