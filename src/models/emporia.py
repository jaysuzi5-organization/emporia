"""
emporia Model and Pydantic Schema

This module defines:
- The SQLAlchemy ORM model for persisting emporia data.
- The Pydantic schema for validating API requests when creating a emporia.

"""

from sqlalchemy import Column, DateTime, Integer, String, Float
from framework.db import Base
from datetime import datetime, UTC
from pydantic import BaseModel
from typing import Optional


class emporia(Base):
    """
    SQLAlchemy ORM model representing a emporia record.

    Attributes:
        id (int): Primary key, unique identifier for the record.
        username (str): Unique username, up to 50 characters. Cannot be null.
        email (str): Unique email address, up to 120 characters. Cannot be null.
        full_name (str | None): Optional full name of the user, up to 100 characters.
        create_date (datetime): Timestamp when the record was created (UTC).
        update_date (datetime): Timestamp when the record was last updated (UTC).

    Notes:
        - `create_date` is automatically set when the record is created.
        - `update_date` is automatically updated whenever the record changes.
    """

    __tablename__ = "emporia"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    instant = Column(DateTime, nullable=False, index=True)
    scale = Column(String(10), nullable=False)
    deviceGid = Column(Integer, nullable=False)
    channelNum = Column(String(20), nullable=False)
    name = Column(String(120), nullable=False, index=True)
    usage = Column(Float, nullable=False)
    unit = Column(String(20), nullable=False)
    percentage = Column(Float, nullable=False)
    create_date = Column(DateTime, default=lambda: datetime.now(UTC))
    update_date = Column(
        DateTime,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC)  # auto-update on change
    )

    def __repr__(self):
        """
        Returns a string representation of the emporia instance.

        Example:
            <emporia(id=1, username='johndoe', email='john@example.com')>
        """
        return f"<emporia(id={self.id}, name='{self.name}')>"



class DeviceUsageCreate(BaseModel):
    """
    Pydantic schema for creating a new device usage entry.

    Attributes:
        instant (datetime): Timestamp of the reading.
        scale (str): Scale of measurement (e.g., '1D').
        deviceGid (int): Device GID.
        channelNum (str): Channel numbers (comma-separated).
        name (str): Name of the device.
        usage (float): Energy usage.
        unit (str): Unit of measurement (e.g., 'KilowattHours').
        percentage (float): Usage percentage.

    Example:
        {
            "instant": "2025-09-09T00:00:00Z",
            "scale": "1D",
            "deviceGid": 138435,
            "channelNum": "1,2,3",
            "name": "Electricity Monitor",
            "usage": 38.39137316071193,
            "unit": "KilowattHours"
            "percentage": 100.0,
        }
    """
    instant: datetime
    scale: str
    deviceGid: int
    channelNum: str
    name: str
    usage: float
    unit: str
    percentage: float
