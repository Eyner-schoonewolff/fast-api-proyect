from sqlalchemy import MetaData, create_engine
from databases import Database

DATABASE_URL = "mysql+pymysql://root@localhost:3300/proyectoFast"

engine = create_engine(DATABASE_URL)

metadata = MetaData()

database = Database(DATABASE_URL)
