from sqlalchemy import create_engine, MetaData
from databases import Database


DATABASE_URL = 'sqlite:///./hablemos_juntos.db'

metadata = MetaData()
database = Database(DATABASE_URL)
engine = create_engine(DATABASE_URL)