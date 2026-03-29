import scrapy

from .ymca_burlington_hamilton import YmcaHamiltonBurlingtonPools


class YmcaHamilton(YmcaHamiltonBurlingtonPools, scrapy.Spider):
    name = "ymca-hamilton"
    calendar_name = "YMCA Hamilton"
    allowed_domains = ["www.ymcahbb.ca"]

    locations: list[str] = ["Hamilton%20Downtown%20Family%20YMCA"]
