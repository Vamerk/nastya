from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import SQLModel, Session, create_engine, select
from typing import List
from datetime import datetime, date
import uvicorn

# from routers import datas
from schemas import *

# Define the models (Assume they are already defined here as per the previous step)

# Database setup
DATABASE_URL = 'postgresql+psycopg2://postgres:admin@localhost:5432/nastya2'
engine = create_engine(DATABASE_URL)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# Dependency for session management
def get_session():
    with Session(engine) as session:
        yield session


app = FastAPI()
#
# app.include_router(datas.router)

# CRUD operations

@app.post("/genders/", response_model=Gender)
def create_gender(gender: Gender, session: Session = Depends(get_session)):
    session.add(gender)
    session.commit()
    session.refresh(gender)
    return gender


@app.get("/genders/", response_model=List[Gender])
def read_genders(session: Session = Depends(get_session)):
    genders = session.exec(select(Gender)).all()
    return genders


@app.post("/diagnoses/", response_model=Diagnosis)
def create_diagnosis(diagnosis: Diagnosis, session: Session = Depends(get_session)):
    session.add(diagnosis)
    session.commit()
    session.refresh(diagnosis)
    return diagnosis


@app.get("/diagnoses/", response_model=List[Diagnosis])
def read_diagnoses(session: Session = Depends(get_session)):
    diagnoses = session.exec(select(Diagnosis)).all()
    return diagnoses


@app.post("/patients/", response_model=Patient)
def create_patient(patient: Patient, session: Session = Depends(get_session)):
    session.add(patient)
    session.commit()
    session.refresh(patient)
    return patient


@app.get("/patients/", response_model=List[Patient])
def read_patients(session: Session = Depends(get_session)):
    patients = session.exec(select(Patient)).all()
    return patients


@app.post("/positions/", response_model=EmployeePosition)
def create_position(position: EmployeePosition, session: Session = Depends(get_session)):
    session.add(position)
    session.commit()
    session.refresh(position)
    return position


@app.get("/positions/", response_model=List[EmployeePosition])
def read_positions(session: Session = Depends(get_session)):
    positions = session.exec(select(EmployeePosition)).all()
    return positions


@app.post("/employees/", response_model=Employee)
def create_employee(employee: Employee, session: Session = Depends(get_session)):
    session.add(employee)
    session.commit()
    session.refresh(employee)
    return employee


@app.get("/employees/", response_model=List[Employee])
def read_employees(session: Session = Depends(get_session)):
    employees = session.exec(select(Employee)).all()
    return employees


@app.post("/internalorders/", response_model=InternalOrder)
def create_internal_order(order: InternalOrder, session: Session = Depends(get_session)):
    session.add(order)
    session.commit()
    session.refresh(order)
    return order


@app.get("/internalorders/", response_model=List[InternalOrder])
def read_internal_orders(session: Session = Depends(get_session)):
    orders = session.exec(select(InternalOrder)).all()
    return orders


@app.post("/brigades/", response_model=Brigade)
def create_brigade(brigade: Brigade, session: Session = Depends(get_session)):
    session.add(brigade)
    session.commit()
    session.refresh(brigade)
    return brigade


@app.get("/brigades/", response_model=List[Brigade])
def read_brigades(session: Session = Depends(get_session)):
    brigades = session.exec(select(Brigade)).all()
    return brigades

@app.post("/shiftrates/", response_model=ShiftRate)
def create_shift_rate(shift_rate: ShiftRate, session: Session = Depends(get_session)):
    session.add(shift_rate)
    session.commit()
    session.refresh(shift_rate)
    return shift_rate

@app.post("/calls/", response_model=Call)
def create_call(call: Call, session: Session = Depends(get_session)):
    session.add(call)
    session.commit()
    session.refresh(call)
    return call


@app.get("/calls/", response_model=List[Call])
def read_calls(session: Session = Depends(get_session)):
    calls = session.exec(select(Call)).all()
    return calls


@app.post("/callresults/", response_model=CallResult)
def create_call_result(result: CallResult, session: Session = Depends(get_session)):
    session.add(result)
    session.commit()
    session.refresh(result)
    return result


@app.get("/callresults/", response_model=List[CallResult])
def read_call_results(session: Session = Depends(get_session)):
    results = session.exec(select(CallResult)).all()
    return results


@app.post("/dispatches/", response_model=Dispatch)
def create_dispatch(dispatch: Dispatch, session: Session = Depends(get_session)):
    session.add(dispatch)
    session.commit()
    session.refresh(dispatch)
    return dispatch


@app.get("/dispatches/", response_model=List[Dispatch])
def read_dispatches(session: Session = Depends(get_session)):
    dispatches = session.exec(select(Dispatch)).all()
    return dispatches

@app.get("/dispatches/{dispatch_date}", response_model=List[dict])
def get_dispatches_by_date(dispatch_date: date, session: Session = Depends(get_session)):
    result = session.exec(
        select(Dispatch, Call, Brigade)
        .join(Call, Dispatch.call_id == Call.id)
        .join(Brigade, Call.brigade_id == Brigade.id)
        .where(Dispatch.dispatch_time.between(
            datetime.combine(dispatch_date, datetime.min.time()),
            datetime.combine(dispatch_date, datetime.max.time())
        ))
    ).all()

    dispatches = []
    for dispatch, call, brigade in result:
        dispatch_info = {
            "call_id": call.id,
            "dispatch_time": dispatch.dispatch_time,
            "brigade_number": brigade.brigade_number,
            "measures_taken": call.measures_taken
        }
        dispatches.append(dispatch_info)

    return dispatches

@app.get("/longest_dispatch/{dispatch_date}", response_model=Optional[dict])
def get_longest_dispatch_by_date(dispatch_date: date, session: Session = Depends(get_session)):
    result = session.exec(
        select(Dispatch, Call, Brigade)
        .join(Call, Dispatch.call_id == Call.id)
        .join(Brigade, Call.brigade_id == Brigade.id)
        .where(Dispatch.dispatch_time.between(
            datetime.combine(dispatch_date, datetime.min.time()),
            datetime.combine(dispatch_date, datetime.max.time())
        ))
        .order_by((Dispatch.arrival_time - Dispatch.dispatch_time).desc())
        .limit(1)
    ).first()

    if result:
        dispatch, call, brigade = result
        longest_dispatch = {
            "call_id": dispatch.call_id,
            "dispatch_time": dispatch.dispatch_time,
            "arrival_time": dispatch.arrival_time,
            "duration": dispatch.arrival_time - dispatch.dispatch_time,
            "brigade_number": brigade.brigade_number,
            "measures_taken": call.measures_taken
        }
        return longest_dispatch
    return None

@app.get("/brigade_employees/{brigade_id}/{dispatch_date}", response_model=List[dict])
def get_brigade_employees_by_date(brigade_id: int, dispatch_date: date, session: Session = Depends(get_session)):
    employees = session.exec(
        select(Employee, EmployeePosition)
        .join(EmployeePosition, Employee.position_id == EmployeePosition.id)
        .where(
            Employee.start_date <= dispatch_date,
            (Employee.end_date.is_(None) | (Employee.end_date >= dispatch_date))
        )
    ).all()

    if not employees:
        raise HTTPException(status_code=404, detail="No employees found for the specified brigade and date")

    response = []
    for employee, position in employees:
        response.append({
            "employee_number": employee.employee_number,
            "first_name": employee.first_name,
            "last_name": employee.last_name,
            "position": position.position_name
        })

    return response


if __name__ == "__main__":
    create_db_and_tables()
    uvicorn.run(app, host="0.0.0.0", port=8000)
