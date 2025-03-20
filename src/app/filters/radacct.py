from datetime import datetime

from fastapi_filter.contrib.sqlalchemy import Filter


class RadacctBaseFilter(Filter):
    username: str | None = None
    acctterminatecause: str | None = None


class RadacctTimeFilter(Filter):
    acctstarttime__gte: datetime | None = None
    acctstoptime__lte: datetime | None = None


class RadacctFilter(RadacctBaseFilter, RadacctTimeFilter): ...
