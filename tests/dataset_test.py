import pprint

from context import pyzzz

from pyzzz import dataset

agents_basic = dataset.load_agents_basic()
pprint.pprint(agents_basic)

skills = dataset.load_skills()
pprint.pprint(skills)

weapons = dataset.load_weapons()
pprint.pprint(weapons)
