from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from app.auth.dependencies import get_current_user
from app.auth.models import User


def require_admin(
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required.",
        )

    return current_user