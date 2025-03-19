from datetime import datetime
from typing import Annotated, NamedTuple

from fastapi import Depends, Query

from app.core.timezone import utc_now


class TimeRangeParams(NamedTuple):
    start_time: datetime
    end_time: datetime


def get_time_range_params(
    start_time: datetime = Query(  # noqa: B008
        default_factory=lambda: utc_now().replace(day=1, hour=0, minute=0, second=0),
        description="Start time, defaults to first day of current month.",
    ),
    end_time: datetime = Query(  # noqa: B008
        default_factory=lambda: utc_now(),
        description="End time, defaults to current time.",
    ),
) -> TimeRangeParams:
    return TimeRangeParams(start_time, end_time)


TimeRangeParamsQuery = Annotated[TimeRangeParams, Depends(get_time_range_params)]
