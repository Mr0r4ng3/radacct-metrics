from datetime import datetime

from app.schemas.base import Schema


class RadacctSchema(Schema):
    radacctid: int
    acctsessionid: str | None = None
    acctuniqueid: str | None = None
    username: str | None = None
    groupname: str | None = None
    realm: str | None = None
    nasipaddress: str | None = None
    nasportid: str | None = None
    nasporttype: str | None = None
    acctstarttime: datetime | None = None
    acctstoptime: datetime | None = None
    acctsessiontime: int | None = None
    acctauthentic: str | None = None
    connectinfo_start: str | None = None
    connectinfo_stop: str | None = None
    acctinputoctets: int | None = None
    acctoutputoctets: int | None = None
    calledstationid: str | None = None
    callingstationid: str | None = None
    acctterminatecause: str | None = None
    servicetype: str | None = None
    framedprotocol: str | None = None
    framedipaddress: str | None = None
    acctstartdelay: int | None = None
    acctstopdelay: int | None = None
    xascendsessionsvrkey: str | None = None
