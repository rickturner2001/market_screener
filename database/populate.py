from classes.database.SP500Database import SP500Database
from database.database_functions.functions import populate_sp500
from config import db_path

sp500_database = SP500Database()
sp500_database.connect_existing_database(db_path / "sp500.sqlite")
populate_sp500(sp500_database, update=True)
