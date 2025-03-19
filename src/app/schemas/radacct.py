from datetime import datetime
from enum import Enum

from app.schemas.base import Schema


class NasPortTypeEnum(Enum):
    Virtual = "Virtual"
    Async = "Async"


class RadacctSchema(Schema):
    radacctid: int
    acctsessionid: str
    acctuniqueid: str
    username: str
    groupname: str
    realm: str
    nasipaddress: str
    nasportid: str
    nasporttype: NasPortTypeEnum
    acctstarttime: datetime
    acctstoptime: datetime
    acctsessiontime: int
    acctauthentic: str
    connectinfo_start: str
    connectinfo_stop: str
    acctinputoctets: int
    acctoutputoctets: int
    calledstationid: str
    callingstationid: str
    acctterminatecause: str
    servicetype: str
    framedprotocol: str
    framedipaddress: str
    acctstartdelay: int
    acctstopdelay: int
    xascendsessionsvrkey: str
