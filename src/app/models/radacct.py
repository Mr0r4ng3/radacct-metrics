from typing import Self

from sqlalchemy import Column, DateTime, Integer, String

from app.core.db.models.base import Model

cached_classes = {}


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

    @classmethod
    def get_model(cls, table_name: str) -> Self:
        if cached_classes.get(table_name) is not None:
            return cached_classes.get(table_name)

        new_model = cls._make_model(table_name)

        cached_classes[table_name] = new_model

        return new_model

    @classmethod
    def _make_model(cls, table_name: str) -> Self:
        class_name = f"Radacct_{table_name}"

        model = type(class_name, (Radacct,), {"__tablename__": table_name})

        return model
