from datetime import datetime, timedelta, UTC
from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session
from sqlalchemy import and_, asc
from framework.db import get_db
from models.emporia import Emporia, EmporiaCreate, EmporiaSearch
from typing import Optional


router = APIRouter()

def serialize_sqlalchemy_obj(obj):
    """
    Convert a SQLAlchemy ORM model instance into a dictionary.

    Args:
        obj: SQLAlchemy model instance.

    Returns:
        dict: Dictionary containing all column names and their values.
    """
    return {column.name: getattr(obj, column.name) for column in obj.__table__.columns}


@router.get("/api/v1/emporia")
def list_emporia(
    page: int = Query(1, ge=1, description="Page number to retrieve"),
    limit: int = Query(10, ge=1, le=100, description="Number of records per page"),
    db: Session = Depends(get_db)
):
    """
    Retrieve a paginated list of emporia records.

    Args:
        page (int): Page number starting from 1.
        limit (int): Maximum number of records to return per page.
        db (Session): SQLAlchemy database session.

    Returns:
        list[dict]: A list of serialized emporia records.
    """
    try:
        offset = (page - 1) * limit
        emporia_records = db.query(Emporia).offset(offset).limit(limit).all()
        return [serialize_sqlalchemy_obj(item) for item in emporia_records]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/api/v1/emporia")
def create_record(
    emporia_data: EmporiaCreate = Body(..., description="Data for the new record"),
    db: Session = Depends(get_db)
):
    """
    Create a new emporia record.

    Args:
        emporia_data (EmporiaCreate): Data model for the record to create.
        db (Session): SQLAlchemy database session.

    Returns:
        dict: The newly created emporia record.
    """
    try:
        data = emporia_data.model_dump(exclude_unset=True)
        new_record = Emporia(**data)
        new_record.create_date = datetime.now(UTC)
        new_record.update_date = datetime.now(UTC)

        db.add(new_record)
        db.commit()
        db.refresh(new_record)
        return serialize_sqlalchemy_obj(new_record)
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/api/v1/emporia/{id}")
def get_emporia_by_id(id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single emporia record by ID.

    Args:
        id (int): The ID of the record.
        db (Session): SQLAlchemy database session.

    Returns:
        dict: The matching emporia record.

    Raises:
        HTTPException: If the record is not found.
    """
    try:
        record = db.query(Emporia).filter(Emporia.id == id).first()
        if not record:
            raise HTTPException(status_code=404, detail=f"emporia with id {id} not found")
        return serialize_sqlalchemy_obj(record)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.put("/api/v1/emporia/{id}")
def update_emporia_full(
    id: int,
    emporia_data: EmporiaCreate = Body(..., description="Updated data for the record"),
    db: Session = Depends(get_db)
):
    """
    Fully update an existing emporia record (all fields required).

    Args:
        id (int): The ID of the record to update.
        emporia_data (EmporiaCreate): Updated record data (all fields).
        db (Session): SQLAlchemy database session.

    Returns:
        dict: The updated emporia record.

    Raises:
        HTTPException: If the record is not found.
    """
    try:
        record = db.query(Emporia).filter(Emporia.id == id).first()
        if not record:
            raise HTTPException(status_code=404, detail=f"emporia with id {id} not found")

        data = emporia_data.model_dump(exclude_unset=False)
        for key, value in data.items():
            setattr(record, key, value)

        record.update_date = datetime.now(UTC)
        db.commit()
        db.refresh(record)
        return serialize_sqlalchemy_obj(record)
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.patch("/api/v1/emporia/{id}")
def update_emporia_partial(
    id: int,
    emporia_data: EmporiaCreate = Body(..., description="Partial updated data for the record"),
    db: Session = Depends(get_db)
):
    """
    Partially update an existing emporia record (only provided fields are updated).

    Args:
        id (int): The ID of the record to update.
        emporia_data (EmporiaCreate): Partial updated data.
        db (Session): SQLAlchemy database session.

    Returns:
        dict: The updated emporia record.

    Raises:
        HTTPException: If the record is not found.
    """
    try:
        record = db.query(Emporia).filter(Emporia.id == id).first()
        if not record:
            raise HTTPException(status_code=404, detail=f"emporia with id {id} not found")

        data = emporia_data.model_dump(exclude_unset=True)
        for key, value in data.items():
            setattr(record, key, value)

        record.update_date = datetime.now(UTC)
        db.commit()
        db.refresh(record)
        return serialize_sqlalchemy_obj(record)
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.delete("/api/v1/emporia/{id}")
def delete_emporia(id: int, db: Session = Depends(get_db)):
    """
    Delete a emporia record by ID.

    Args:
        id (int): The ID of the record to delete.
        db (Session): SQLAlchemy database session.

    Returns:
        dict: Confirmation message.

    Raises:
        HTTPException: If the record is not found.
    """
    try:
        record = db.query(Emporia).filter(Emporia.id == id).first()
        if not record:
            raise HTTPException(status_code=404, detail=f"emporia with id {id} not found")

        db.delete(record)
        db.commit()
        return {"detail": f"emporia with id {id} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/api/v1/emporia/search")
def search_emporia(
    search_data: EmporiaSearch = Body(..., description="Search criteria"),
    db: Session = Depends(get_db)
):
    """
    Search for records matching any of the provided fields.
    """
    try:
        filters = []
        data = search_data.model_dump(exclude_unset=True)

        # Handle optional start_date / end_date against emporia.instant
        start_date: Optional[datetime] = data.pop("start_date", None)
        end_date: Optional[datetime] = data.pop("end_date", None)

        if start_date:
            filters.append(EmporiaSearch.instant >= start_date)
        if end_date:
            filters.append(EmporiaSearch.instant <= end_date)

        # Build OR conditions for matching any field
        for field, value in data.items():
            if hasattr(EmporiaSearch, field):
                column = getattr(EmporiaSearch, field)
                filters.append(column == value)

        query = db.query(EmporiaSearch).filter(and_(*filters))
        query = query.order_by(asc(EmporiaSearch.instant))
        results = query.all()

        return [serialize_sqlalchemy_obj(record) for record in results]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")