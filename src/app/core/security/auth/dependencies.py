from typing import Annotated

from fastapi import Depends

from app.core.security.auth.func import get_current_active_user
from app.schemas.users import UserPublic

UserDep = Annotated[UserPublic, Depends(get_current_active_user)]
