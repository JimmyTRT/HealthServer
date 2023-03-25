from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os
from sqlalchemy.pool import StaticPool

from .models import Base

# if os.environ.get('DATABASE_URL'):
#     print(f"os used {os.environ.get('DATABASE_URL')}")
#     engine = create_engine(os.environ.get('DATABASE_URL'))
# else:
#     print('sqlite')
engine = create_engine('sqlite:///test.db', echo=True)


"""
Temp database in geheugen om niet altijd de database te moeten wissen op disk
"""
#engine = create_engine('sqlite:///:memory:', echo=True, poolclass=StaticPool)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
