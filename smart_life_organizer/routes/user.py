from typing import List, Union

from fastapi import APIRouter, Request, Depends, HTTPException
from sqlmodel import Session, select, or_

from ..models.user import UserDB
from ..schemas.user import UserCreate, UserResponse, UserPasswordPatch
from ..db import get_session
from ..security import (
    get_current_admin_user,
    get_current_fresh_user,
    get_current_active_user,
    get_current_user,
    get_password_hash,
)

router = APIRouter()


@router.get("/", response_model=List[UserResponse], dependencies=[Depends(get_current_admin_user)])
async def list_users(*, session: Session = Depends(get_session)):
    users = session.exec(select(UserDB)).all()
    return users


@router.post("/", response_model=UserResponse, dependencies=[Depends(get_current_admin_user)])
async def create_user(*, session: Session = Depends(get_session), user: UserCreate):
    existing_user = session.exec(select(UserDB).where(UserDB.username == user.username)).first()
    if existing_user:
        raise HTTPException(status_code=422, detail="Username already exists")

    db_user = UserDB(
        username=user.username,
        email=user.email,
        phone_number=user.phone_number,
        password_hash=get_password_hash(user.password),
        profile_picture=user.profile_picture,
        first_name=user.first_name,
        last_name=user.last_name,
        gender=user.gender
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.patch("/{user_id}/password/", response_model=UserResponse, dependencies=[Depends(get_current_fresh_user)])
async def update_user_password(
    *,
    user_id: int,
    session: Session = Depends(get_session),
    request: Request,
    patch: UserPasswordPatch,
):
    user = session.get(UserDB, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    current_user: UserDB = get_current_user(request=request)
    if user.user_id != current_user.user_id and not current_user.superuser:
        raise HTTPException(
            status_code=403, detail="You can't update this user's password"
        )

    if patch.password != patch.password_confirm:
        raise HTTPException(status_code=400, detail="Passwords don't match")

    user.password_hash = get_password_hash(patch.password)
    session.commit()
    session.refresh(user)
    return user


@router.get("/{user_id_or_username}/", response_model=UserResponse, dependencies=[Depends(get_current_active_user)])
async def query_user(
    *, session: Session = Depends(get_session), user_id_or_username: Union[str, int]
):
    statement = select(UserDB).where(
        or_(
            UserDB.user_id == user_id_or_username,
            UserDB.username == user_id_or_username,
        )
    )
    user = session.exec(statement).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{user_id}/", dependencies=[Depends(get_current_admin_user)])
def delete_user(
    *, session: Session = Depends(get_session), request: Request, user_id: int
):
    user = session.get(UserDB, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    current_user = get_current_user(request=request)
    if user.user_id == current_user.user_id:
        raise HTTPException(
            status_code=403, detail="You can't delete yourself"
        )

    session.delete(user)
    session.commit()
    return {"ok": True}