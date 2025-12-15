from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

DATABASE_URL = 'postgresql://postgres:1234567890@localhost:5432/restaurant_management'

engine = create_engine(DATABASE_URL)

Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)
