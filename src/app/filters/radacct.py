from datetime import datetime

from fastapi_filter.contrib.sqlalchemy import Filter


class RadacctBaseFilter(Filter):
    username: str | None = None
    acctterminatecause: str | None = None


class RadacctTimeFilter(Filter):
    acctstarttime__gte: datetime
    acctstoptime__lte: datetime


class RadacctFilter(RadacctBaseFilter, RadacctTimeFilter): ...
