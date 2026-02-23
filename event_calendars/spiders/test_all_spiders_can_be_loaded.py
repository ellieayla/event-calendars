from scrapy.utils.project import get_project_settings
from scrapy.spiderloader import get_spider_loader
from scrapy.crawler import AsyncCrawlerProcess

def test_spider_loader() -> None:
    settings = get_project_settings()
    spider_loader = get_spider_loader(settings)
    settings.set("LOG_LEVEL", "WARNING")  # hide chatty logs during normal startup
    crawler_process = AsyncCrawlerProcess(settings)

    for spider_name in sorted(spider_loader.list()):
        crawler_process.crawl(spider_name)

    crawler_process._graceful_stop_reactor() # pyright: ignore[reportPrivateUsage]
