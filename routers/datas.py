from datetime import date
from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import SQLModel, Session, create_engine, select
from main import get_session
from schemas import *

router = APIRouter(
    prefix="/data",
    tags=["data"]
)

@router.get("/dispatches/{dispatch_date}", response_model=List[dict])
def get_dispatches_by_date(dispatch_date: date, session: Session = Depends(get_session)):
    result = session.exec(
        select(Call).where(
            Call.call_date_time.between(
                datetime.combine(dispatch_date, datetime.min.time()),
                datetime.combine(dispatch_date, datetime.max.time())
            )
        ).join(Dispatch)
    ).all()

    dispatches = []
    for call in result:
        dispatch = {
            "call_id": call.id,
            "dispatch_time": call.dispatches[0].dispatch_time,
            "brigade_number": call.brigade.brigade_number,
            "measures_taken": call.measures_taken
        }
        dispatches.append(dispatch)

    return dispatches

@router.get("/longest_dispatch/{dispatch_date}", response_model=Optional[dict])
def get_longest_dispatch_by_date(dispatch_date: date, session: Session = Depends(get_session)):
    result = session.exec(
        select(Dispatch).where(
            Dispatch.dispatch_time.between(
                datetime.combine(dispatch_date, datetime.min.time()),
                datetime.combine(dispatch_date, datetime.max.time())
            )
        ).order_by((Dispatch.arrival_time - Dispatch.dispatch_time).desc()).limit(1)
    ).first()

    if result:
        longest_dispatch = {
            "call_id": result.call_id,
            "dispatch_time": result.dispatch_time,
            "arrival_time": result.arrival_time,
            "duration": result.arrival_time - result.dispatch_time,
            "brigade_number": result.call.brigade.brigade_number,
            "measures_taken": result.call.measures_taken
        }
        return longest_dispatch
    return None

@router.get("/brigade_employees/{brigade_id}/{dispatch_date}", response_model=List[dict])
def get_brigade_employees_by_date(brigade_id: int, dispatch_date: date, session: Session = Depends(get_session)):
    brigade = session.exec(
        select(Brigade).where(Brigade.id == brigade_id)
    ).first()

    if not brigade:
        raise HTTPException(status_code=404, detail="Brigade not found")

    employees = []
    for employee in brigade.employees:
        if employee.start_date <= dispatch_date and (not employee.end_date or employee.end_date >= dispatch_date):
            emp = {
                "employee_number": employee.employee_number,
                "first_name": employee.first_name,
                "last_name": employee.last_name,
                "position": employee.position.position_name
            }
            employees.append(emp)

    return employees