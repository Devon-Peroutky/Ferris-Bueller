import os
import sys
from sqlalchemy import MetaData, Table
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()
m = MetaData()

# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
db = create_engine('mysql://root:arsenal@localhost/Ferris')
m.reflect(db)

# Load the tables
events = Table('events', m, autoload=True, autoload_with=db)
interests = Table('interests', m, autoload=True, autoload_with=db)
userInterests = Table('userInterests', m, autoload=True, autoload_with=db)
users = Table('users', m, autoload=True, autoload_with=db)

class Event(Base):
    __tablename__ = 'events'

    Id = Column(Integer, primary_key=True)
    EventId = Column(String)
    Title = Column(String)
    Venue = Column(String)
    VenueAddress = Column(String)
    Category = Column(String)
    StartTime = Column(String)
    Url = Column(String)
    Image = Column(String)
    UploadDate = Column(String)

    def __repr__(self):
        return "<User(Id='%s', EventId='%s', Title='%s')>" % ( self.Id, self.EventId, self.Title)

class Interest(Base):
    __tablename__ = 'interests'

    Interest_Id = Column(Integer, primary_key=True)
    Interest = Column(String)

class UserInterest(Base):
    __tablename__ = 'userinterests'

    User_Id = Column(Integer, primary_key=True)
    Interest_Id = Column(Integer)

class User(Base):
    __tablename__ = 'users'

    User_Id = Column(Integer, primary_key=True)
    First_Name = Column(String)
    Last_Name = Column(String)
    Phone_Number = Column(Integer)
    Location = Column(String)
    Date_Joined = Column(String)
