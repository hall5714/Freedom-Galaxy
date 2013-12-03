"""
This module parses the provided data files, maps the data to our
ORM, and inserts the neccesary objects to populate the database.

Tables/data files currently implemented:
    - Characters
    - Environs
    - MilitaryUnits
    - Planets
    - Possessions
    - Races

To-do list for current ORM:
    - Missions
    - Environs: figure out how soverigns work in the dat_file
    - Possesssions: figure out what string stats mean (stat1-32)

We could implement these charts in the database and use stored
procedures to return combat/detection results:
    - Character Combat Chart
    - Detection Chart
    - Military Combat Chart

"""
import re

import orm

def data_parser(file_name):
    """
    For given file_name, parse lines into a list of lists of data.

    Uses the regular expression '[A-Z0-9/ "'*.\-]+' to capture
    groups of data; ignores empty lines and those starting with '#'

    Regular expression explanation: [] indicates a character set, with
    the +, it matches any string consisting of one or more of those
    characters. Using the IGNORECASE flag, we need only specify the
    alphabet by the range A-Z, the digits 0-9, forward slash, space,
    double quote, single quote, asterisk, period, and hyphen. Note
    that the last is the only one that needs to be escaped inside a
    character set. The expression is encapsulated by triple quotes to
    allow for easy inclusing of the quote characters, and is made
    'raw' with the r prefix, so that the backslash can be used
    literally. All these characters were founda as valid data in some
    data file.

    This function replaces those that were found in dataSnag.py

    """
    data_list = []
    regex = re.compile(r"""[A-Z0-9/ "'*.\-]+""", flags=re.IGNORECASE)
    with open(file_name) as data:
        for line in data:  # iterate over lines in the file
            if not line.strip().startswith('#') and line.strip():
            # not a comment and exists
                data_list.append([match.strip() for match in
                                  re.findall(regex, line)])
    return data_list

def load_database():
    """
    This function creates a database session to which it adds rows
    of data to the database.

    The tables dict represents a mapping from the data files to our
    ORM. Its outermost keys represent the tables defined in orm, the
    values are themselves dicts. This inner dicts contain the path
    (that is, name of the data file in ./dat_files), a defaults dict
    that allows specification of columns whose values are not in the
    data files, and a keys tuple which maps linearly from the table's
    columns to the position of the data field in the file.

    """
    session = orm.Session()
    tables = {
        'Characters': {
            'path': 'charactr.dat',
            'defaults': {'wounds': 0, 'detected': False, 'possession': False,
                         'active': True, 'captive': False},
            'keys': ('name', 'gif', 'title', 'race', 'side', 'combat',
                     'endurance', 'intelligence', 'leadership', 'diplomacy',
                     'navigation', 'homeworld', 'bonuses')},
        'Environs': {
            'path': 'environ.dat',
            'defaults': {},
            'keys': ('id_', 'type_', 'size', 'race_name', 'starfaring',
                     'resources', 'starresources', 'monster', 'coup_sov')},
        'MilitaryUnits': {
            'path': 'military_units.dat',
            'defaults': {'wounds': 0},
            'keys': ('type_', 'side', 'environ_combat', 'space_combat',
                     'mobile')},
        'Planets': {
            'path': 'planet.dat',
            'defaults': {},
            'keys': ('id_', 'name', 'race', 'sloyalty', 'aloyalty',
                     'environs_num')},
        'Possessions': {
            'path': 'possessn.dat',
            'defaults': {'damaged': False},
            'keys': ('type_', 'name', 'gif', 'stat1', 'stat2', 'stat3',
                     'stat4', 'owner_name')},
        'Races': {
            'path': 'races.dat',
            'defaults': {},
            'keys': ('name', 'environ', 'combat', 'endurance', 'firefight')}
    }

    for table, info in tables.iteritems():
        for values in data_parser('./dat_files/'+info['path']):
            session.add(getattr(orm, table)(**dict(
                zip(info['keys'], values), **info['defaults'])))
    session.commit()

    for planet_id in session.query(orm.Planets.id_).all():
        session.add(orm.Environs(id_=planet_id[0]*10, type_='O', size=50))
    session.commit()
