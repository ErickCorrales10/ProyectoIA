from databases import Database
from sqlalchemy import create_engine, MetaData

DATABASE_URL = 'sqlite:///./hablemos_juntos.db'

database = Database(DATABASE_URL)
metadata = MetaData()
engine = create_engine(DATABASE_URL)
metadata.create_all(engine)