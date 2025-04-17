from typing import List, Union

from fastapi import APIRouter, Request, Depends, HTTPException
from sqlmodel import Session, or_, select

from ..db import get_session
from ..models.content import Content, ContentIncoming, ContentResponse
from ..security import User, get_current_user, get_current_active_user

router = APIRouter()


@router.get("/", response_model=List[ContentResponse])
async def list_contents(*, session: Session = Depends(get_session)):
    contents = session.exec(select(Content)).all()
    return contents


@router.get("/{id_or_slug}/", response_model=ContentResponse)
async def query_content(
    *, id_or_slug: Union[str, int], session: Session = Depends(get_session)
):
    content = session.exec(
        select(Content).where(
            or_(
                Content.id == id_or_slug,
                Content.slug == id_or_slug,
            )
        )
    ).first()

    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    return content


@router.post("/", response_model=ContentResponse)
async def create_content(
    *,
    session: Session = Depends(get_session),
    request: Request,
    content: ContentIncoming,
    current_user: User = Depends(get_current_active_user),
):
    db_content = Content.from_orm(content)
    db_content.user_id = current_user.id
    session.add(db_content)
    session.commit()
    session.refresh(db_content)
    return db_content


@router.patch("/{content_id}/", response_model=ContentResponse)
async def update_content(
    *,
    content_id: int,
    session: Session = Depends(get_session),
    request: Request,
    patch: ContentIncoming,
    current_user: User = Depends(get_current_active_user),
):
    content = session.get(Content, content_id)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")

    if content.user_id != current_user.id and not current_user.superuser:
        raise HTTPException(
            status_code=403, detail="You don't own this content"
        )

    patch_data = patch.dict(exclude_unset=True)
    for key, value in patch_data.items():
        setattr(content, key, value)

    session.commit()
    session.refresh(content)
    return content


@router.delete("/{content_id}/")
def delete_content(
    *, session: Session = Depends(get_session), request: Request, content_id: int, current_user: User = Depends(get_current_active_user)
):
    content = session.get(Content, content_id)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")

    if content.user_id != current_user.id and not current_user.superuser:
        raise HTTPException(
            status_code=403, detail="You don't own this content"
        )

    session.delete(content)
    session.commit()
    return {"ok": True}