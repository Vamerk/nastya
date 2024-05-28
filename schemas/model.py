from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

class Gender(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    gender: str

class Diagnosis(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    initial_diagnosis: str

class Patient(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    approximate_age: int
    address: str
    gender_id: Optional[int] = Field(default=None, foreign_key="gender.id")
    initial_diagnosis_id: Optional[int] = Field(default=None, foreign_key="diagnosis.id")

class EmployeePosition(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    position_name: str

class ShiftRate(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    rate: float

class Employee(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_number: int
    first_name: str
    last_name: str
    middle_name: Optional[str]
    date_of_birth: datetime
    position_id: Optional[int] = Field(default=None, foreign_key="employeeposition.id")
    start_date: datetime
    end_date: Optional[datetime]
    rate_id: Optional[int] = Field(default=None, foreign_key="shiftrate.id")

class InternalOrder(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    order_number: int
    order_date: datetime
    shift_start_date: datetime
    shift_end_date: datetime

class Brigade(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    brigade_number: int
    specialization: str
    internal_order_id: Optional[int] = Field(default=None, foreign_key="internalorder.id")
    # employees: List[Employee] = Relationship(back_populates="brigade")

class Call(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    call_date_time: datetime
    patient_id: Optional[int] = Field(default=None, foreign_key="patient.id")
    # patient: Optional[Patient] = Relationship(back_populates="calls")
    brigade_id: Optional[int] = Field(default=None, foreign_key="brigade.id")
    # brigade: Optional[Brigade] = Relationship(back_populates="calls")
    measures_taken: str

class CallResult(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    result_description: str

class Dispatch(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    dispatch_time: datetime
    arrival_time: datetime
    call_id: Optional[int] = Field(default=None, foreign_key="call.id")
    # call: Optional[Call] = Relationship(back_populates="dispatches")
    result_id: Optional[int] = Field(default=None, foreign_key="callresult.id")
    # result: Optional[CallResult] = Relationship(back_populates="dispatches")
