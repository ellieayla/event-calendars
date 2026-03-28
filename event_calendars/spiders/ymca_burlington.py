import scrapy

from .ymca_burlington_hamilton import YmcaHamiltonBurlingtonPools


class YmcaBurlington(YmcaHamiltonBurlingtonPools, scrapy.Spider):
    name = "ymca-burlington"
    allowed_domains = ["www.ymcahbb.ca"]

    skip_in_runall = False

    locations: list[str] = ["Ron%20Edwards%20Family%20YMCA"]
