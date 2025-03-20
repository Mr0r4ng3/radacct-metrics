from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.db.database import get_db
from app.core.db.radius_db import get_db as get_radius_db

DbDep = Annotated[Session, Depends(get_db)]
RadiusDbDep = Annotated[Session, Depends(get_radius_db)]
