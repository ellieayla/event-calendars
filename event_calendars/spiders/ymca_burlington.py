import scrapy

from .ymca_burlington_hamilton import YmcaHamiltonBurlingtonPools


class YmcaBurlington(YmcaHamiltonBurlingtonPools, scrapy.Spider):
    name = "ymca-burlington"
    calendar_name = "YMCA Burlington"
    allowed_domains = ["www.ymcahbb.ca"]

    locations: list[str] = ["Ron%20Edwards%20Family%20YMCA"]
