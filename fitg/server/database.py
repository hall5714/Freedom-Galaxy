"""
This is the main database singleton, running in a single instance
of fitg.py --server

The makes the ORM backend, and allows for execution of queries. It's
currently in a highly alpha stage, as I make my way through the
provided data files, and figure out on-the-fly an ER design, and the
use of SQLAlchemy.

When this is done, a parser should be written (or adapted from Greg's
code) to populate these tables from the CSV data files.

"""

from sqlalchemy import (create_engine, Table, Column, Integer, String,
                        MetaData, ForeignKey)
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import realtionship, backref, sessionmaker

# Make the engine
engine = create_engine('sqlite:///:memory:', echo=True)

# Mixin for ID as primary key
class UniqueMixin(object):
    id = Column(Integer, primary_key=True)

# Mixin for name
class NameMixin(object):
    name = Column(String)

# Get a base class for the database
class Base(Object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

Base = declarative_base(cls=Base)

# Define database tables
class Game(Base, UniqueMixin):
    scenario = relationship('Scenario', backref='game')
    client_id_left = Column(Integer, ForeignKey('client.id'))
    client_id_right = Column(Integer, ForeignKey('client.id'))

class Client(Base, UniqueMixin):
    host = Column(String)
    port = Column(Integer)
    player_id = Column(Integer, ForeignKey('player.id'))
    player = relationship('Player', backref='client')

class Player(Base, UniqueMixin):
    side = Column(Integer, ForeignKey('side.id'))
    status = Coulmn(Integer, ForeignKey('status.id'))

class Side(Base, UniqueMixin, NameMixin):
    # Imperial/Rebel
    pass

class Status(Base, UniqueMixin, NameMixin):
    # Phasing/Non-phasing
    pass

class Scenario(Base, UniqueMixin, NameMixin):
    game_type = Column(String)
    # Needs start and end conditions

class Galaxy(Base, UniqueMixin):
    province_id = Column(Integer, ForeignKey('province.id'))
    provinces = relationship('Province', backref='galaxy')

class Province(Base, UniqueMixin):
    system_id = Column(Integer, ForeignKey('system.id'))
    systems = relationship('System', backref='province')
    
class System(Base, UniqueMixin, NameMixin):
    gal_x = Column(Integer)
    gal_y = Column(Integer)
    neighbors = relationship('System', secondary='Neighbors',
                             primaryjoin=id='neighbors.system_id_left',
                             secondaryjoin=id='neighbors.system_id_right')
    # This "self-referential many-to-many" relationship needs fixing
    planets = relationship('Planet', backref='system')

class Neighbors(Base):
    system_id_left = Column(Integer, ForeignKey('system.id'), primary_key=True)
    system_id_right = Column(Integer, ForeignKey('system.id'), primary_key=True)
    distance = Column(Integer)

class Planet(Base, UniqueMixin, NameMixin):
    race_id = Column(Integer, ForeignKey('race.id'))
    s_loyalty = Column(Integer)
    a_loyalty = Column(Integer)
    environs = relationship('Environ', ForeignKey('environ.id'), backref='planet')

class Space(Base):
    pass

class Environ(Base, UniqueMixin):
    type_id = Column(Integer, ForeignKey('environ_type.id'))
    size = Column(Integer)
    race_id = Column(Integer, ForeignKey('race.id'))
    resources = Column(Integer)
    creature_id = Column(Integer, ForeignKey('creature.id'))
    politics = Column(Integer)

class EnvironType(Base, UniqueMixin, NameMixin):
    pass

class Race(Base, UniqueMixin, NameMixin):
    type_id = Column(Integer, ForeignKey('environ_type.id'))

class Creature(Base, UniqueMixin, NameMixin):
    pass

# Create all tables not yet created
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
