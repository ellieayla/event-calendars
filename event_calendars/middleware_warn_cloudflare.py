# If a request was blocked by Cloudflare,
# don't try to bypass it.
# Log this clearly.

from logging import getLogger

from scrapy import Request
from scrapy.exceptions import CloseSpider
from scrapy.http import Response

logger = getLogger(__name__)


class DetectCloudflareIntercepted:
    """
    Inspect responses to determine whether one has been replaced with a Cloudflare challenge page.
    Log this, so we know to stop trying.
    """

    def process_response(self, request: Request, response: Response) -> Response:
        if response.status in (403,):
            logger.warning(f"Response to url {request.url} is {response.status}: {response.text[:50]=}")

            if "cloudflare.com" in response.text:
                raise CloseSpider(f"{response.status} for {request.url} - probable cloudflare intercept.")

        return response
