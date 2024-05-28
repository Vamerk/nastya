from datetime import date
from fastapi import HTTPException
from typing import List, Type, Optional

from sqlmodel import Session, select, SQLModel, create_engine, func, desc

from .model import *


db_name = 'nastya'
db_user = 'postgres'
db_pass = 'admin'

db_url = f'postgresql+psycopg2://postgres:admin@localhost:5432/nastya'