from sqlalchemy import create_engine
from api_database import Base
from config import db_path

database_path = "sqlite:///" + str(db_path) + "/sp500.sqlite"
engine = create_engine(database_path, echo=False, future=True)
Base.metadata.create_all(engine)
