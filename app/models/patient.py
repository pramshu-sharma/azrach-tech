from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Enum,
    func
)


from app.core.database import Base

PATIENT_STATUS = 'Pending', 'Checked', 'Failed'

class Patient(Base):
    __tablename__ = 'patients'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    notes = Column(Text, nullable=True)
    check_datetime = Column(DateTime, nullable=False)
    status = Column(
        Enum(*PATIENT_STATUS, name='patient_status'),
        nullable=False,
        server_default='Pending'
    )
    created_at = Column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
