# pyright: reportUnusedImport=false

from . import (
    burlington_hamilton_ymca,
    burlington_pools,
    cycleto,
    httpbin,
    toronto_community_bikeways,
    whoami,
)

from .registry import register

__all__ = ["register"]
