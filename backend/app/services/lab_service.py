from sqlalchemy.orm import Session

from app.common.exceptions import BusinessException
from app.common.response import PageResponse
from app.models.equipment import Equipment
from app.models.lab import Lab
from app.models.reservation import Reservation
from app.schemas.lab import LabCreateRequest, LabResponse, LabUpdateRequest


def get_lab_page_list(
    db: Session,
    page: int,
    page_size: int,
    keywords: str | None = None,
    status: int | None = None,
):
    """分页模糊查询列表"""
    # select * from lab where name like '%计算机%';
    query = db.query(Lab)
    if keywords:
        query = query.filter(Lab.name.ilike(f"%{keywords}%"))
    if status:
        query = query.filter(Lab.status == status)
    total = query.count()
    items = (
        query.order_by(Lab.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    return PageResponse(
        list=[LabResponse.model_validate(item) for item in items], total=total
    )


def get_lab(db: Session, lab_id: int):
    lab = db.query(Lab).filter(Lab.id == lab_id).first()
    if not lab:
        raise BusinessException(message="实验室不存在")
    return LabResponse.model_validate(lab)


def create_lab(db: Session, data: LabCreateRequest):
    exists = db.query(Lab).filter(Lab.name == data.name).first()
    if exists:
        raise BusinessException(message="实验室名称已存在")

    lab = Lab(**data.model_dump())
    db.add(lab)
    db.commit()
    db.refresh(lab)
    return LabResponse.model_validate(lab)


def update_lab(db: Session, lab_id: int, data: LabUpdateRequest):
    lab = db.query(Lab).filter(Lab.id == lab_id).first()
    if not lab:
        raise BusinessException(message="实验室不存在")

    payload = data.model_dump(exclude_none=True)
    if "name" in payload:
        exists = (
            db.query(Lab).filter(Lab.name == payload["name"], Lab.id != lab_id).first()
        )
        if exists:
            raise BusinessException(message="实验室名称已存在")

    for field, value in payload.items():
        setattr(lab, field, value)
    db.commit()
    db.refresh(lab)
    return LabResponse.model_validate(lab)


def delete_lab(db: Session, lab_id: int):
    lab = db.query(Lab).filter(Lab.id == lab_id).first()
    if not lab:
        raise BusinessException(message="实验室不存在")

    has_reservations = (
        db.query(Reservation.id).filter(Reservation.lab_id == lab_id).first()
    )
    has_equipments = (
        db.query(Equipment.id).filter(Equipment.lab_id == lab_id).first()
    )
    if has_reservations or has_equipments:
        raise BusinessException(
            message="实验室存在关联的预约或设备，无法删除，请先处理关联记录",
            code=400,
        )

    db.delete(lab)
    db.commit()
