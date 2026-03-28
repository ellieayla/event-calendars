import scrapy

from .ymca_burlington_hamilton import YmcaHamiltonBurlingtonPools


class YmcaHamilton(YmcaHamiltonBurlingtonPools, scrapy.Spider):
    name = "ymca-hamilton"
    allowed_domains = ["www.ymcahbb.ca"]

    skip_in_runall = False

    locations: list[str] = ["Hamilton%20Downtown%20Family%20YMCA"]
