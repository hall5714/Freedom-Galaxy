"""
This defines the database schema using SQLAlchemy's ORM.
"""

from sqlalchemy import (create_engine, Column, Integer, String,
                        Boolean, ForeignKey)
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import relationship, backref, sessionmaker

# Make the engine
engine = create_engine('sqlite:///Freedom.db')

# Mixin for ID as primary key
class IDMixin(object):
    id_ = Column(Integer, primary_key=True)

# Mixin for name
class NameMixin(object):
    name = Column(String)

# Mixin for a unique name used as a PK
class UniqueNameMixin(object):
    name = Column(String, primary_key=True)

# Get a base class for the database
class Base(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

Base = declarative_base(cls=Base)

class Characters(Base, UniqueNameMixin):
    gif = Column(String)  #Does the DB need this?
    title = Column(String)  #Long title of character
    race = Column(String)  #Character's Race
    side = Column(String)  #Team: 'Rebel' or 'Emperial'
    combat = Column(Integer)  #Combat strength
    endurance = Column(Integer)  #Endurance rating
    intelligence = Column(Integer)  #Intelligence rating
    leadership = Column(Integer)  #Leadership rating
    diplomacy = Column(Integer)  #Diplomacy rating
    navigation = Column(Integer)  #Navigation rating
    homeworld = Column(String)  #Character's Homeworld
    bonuses = Column(String)  #Special Bonuses, unclear format
    wounds = Column(Integer)  #Num of wounds
    detected = Column(Boolean)
    possession = Column(Boolean)
    active = Column(Boolean)
    captive = Column(Boolean)
    stack_id = Column(Integer, ForeignKey('stacks.id_'))
    stack = relationship('Stacks', backref=backref('characters',
                                                   order_by=combat))
    def __repr__(self):
        return "<Character('{0}', '{1}', '{2}')>".format(self.name,
                                                         self.title,
                                                         self.side)

class Environs(Base, IDMixin):
    type_ = Column(String)
    size = Column(Integer)
    starfaring = Column(Integer)
    resources = Column(Integer)
    starresources = Column(Integer)
    monster = Column(String)
    coup = Column(Integer)
    sov = Column(Integer)
    planet_id = Column(Integer, ForeignKey('planets.id_'))
    planet = relationship('Planets', backref=backref('environs',
                                                     order_by=lambda:
                                                     Environs.id_))
    race_name = Column(String, ForeignKey('races.name'))
    race = relationship('Races', backref=backref('environs',
                                                 order_by=lambda:
                                                 Environs.id_))

    def __repr__(self):
        return "<Environ('{0}', '{1}', '{2}')>".format(self.id_,
                                                       self.type_,
                                                       self.size)

class MilitaryUnits(Base, IDMixin):
    side = Column(String)
    type_ = Column(String)
    environ_combat = Column(Integer)
    space_combat = Column(Integer)
    mobile = Column(Integer)
    wounds = Column(Integer)
    stack_id = Column(Integer, ForeignKey('stacks.id_'))
    stack = relationship('Stacks', backref=backref('militaryunits',
                                                  order_by=type_))

    def __repr__(self):
        return "<MilitaryUnit('{0}', '{1}', '{2}')>".format(self.id_,
                                                            self.type_,
                                                            self.side)

class Missions(Base, IDMixin):
    type_ = Column(String)
    stack_id = Column(Integer, ForeignKey('stacks.id_'))
    stack = relationship('Stacks', backref=backref('missions',
                                                   order_by=lambda:
                                                   Missions.id_))

    def __init__(self, type_, stack_id):
        self.type_ = type_
        self.stack_id = stack_id_

    def __repr__(self):
        return "<Mission('{0}', '{1}', '{2}')>".format(self.id_,
                                                       self.type_,
                                                       self.stack_id)

class Planets(Base, IDMixin, NameMixin):
    race = Column(String)
    sloyalty = Column(Integer)
    aloyalty = Column(Integer)
    environs_num = Column(Integer)

    def __repr__(self):
        return "<Planet('{0}', '{1}', '{2}')>".format(self.id_,
                                                      self.race,
                                                      self.environs_num)

class Possessions(Base, UniqueNameMixin):
    type_ = Column(String)  # Type_ of possession.
    gif = Column(String)  # gif related to the possession.
    stat1 = Column(Integer)  # First stat.
    stat2 = Column(Integer)  # Second stat.
    stat3 = Column(Integer)  # Third stat.
    stat4 = Column(Integer)  # Fourth stat.
    damaged = Column(Boolean)  # Whether the possession is damaged. This
                               # really only applies to starships.
    owner_name = Column(String, ForeignKey('characters.name'))
    owner = relationship('Characters', backref=backref('possessions',
                                                       order_by=lambda:
                                                       Possessions.name))

    def __repr__(self):
        return "<Possession('{0}', '{1}', '{2}')>".format(self.type_,
                                                          self.name,
                                                          self.stat1)

class Races(Base, UniqueNameMixin):
    environ = Column(String, primary_key=True)
    combat = Column(Integer)
    endurance = Column(Integer)
    firefight = Column(Boolean)

    def __repr__(self):
        return "<Race('{0}', '{1}', '{2}')>".format(self.name,
                                                    self.environ,
                                                    self.combat)

class Stacks(Base, IDMixin):
    location_id = Column(Integer, ForeignKey('environs.id_'))
    location = relationship('Environs', backref=backref('stacks',
                                                        order_by=lambda:
                                                        Stacks.id_))

    def __init__(self, location_id):
        self.location_id = location_id

    def __repr__(self):
        return "<Stack('{0}', '{1}')>".format(self.id_, self.location)

    def size(self):
        return len(self.characters) + len(self.militaryunits)

    def spaceship(self):
        for character in self.characters:
            for possession in character.possessions:
                if possession.type_ == 'spaceship':
                    return possession
        return None

    def stack_detection(self):  # Check if any characters in the
        for character in self.characters:  # stack are detected.
            if character.detected == True:
                return True
        return None
    # function to add unit to stack, check if not already in another
    # stack, if so, remove?

    def find_stack_leader(self):  # stack leader will be the character with
        leadership_rating = 0  # the highest leadership rating
        for character in self.characters:
            if character.leadership > leadership_rating:
                leadership_rating = character.leadership
        return leadership_rating

# Create all tables not yet created
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
