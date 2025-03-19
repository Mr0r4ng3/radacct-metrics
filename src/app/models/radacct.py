from sqlalchemy import Column, DateTime, Integer, String

from app.core.db.models.base import Model


class Radacct(Model):
    __abstract__ = True

    radacctid = Column(Integer, primary_key=True)
    acctsessionid = Column(String)
    acctuniqueid = Column(String)
    username = Column(String)
    groupname = Column(String)
    realm = Column(String)
    nasipaddress = Column(String)
    nasportid = Column(String)
    nasporttype = Column(String)
    acctstarttime = Column(DateTime)
    acctstoptime = Column(DateTime)
    acctsessiontime = Column(Integer)
    acctauthentic = Column(String)
    connectinfo_start = Column(String)
    connectinfo_stop = Column(String)
    acctinputoctets = Column(Integer)
    acctoutputoctets = Column(Integer)
    calledstationid = Column(String)
    callingstationid = Column(String)
    acctterminatecause = Column(String)
    servicetype = Column(String)
    framedprotocol = Column(String)
    framedipaddress = Column(String)
    acctstartdelay = Column(Integer)
    acctstopdelay = Column(Integer)
    xascendsessionsvrkey = Column(String)
