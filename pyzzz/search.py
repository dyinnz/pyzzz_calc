import heapq

from pyzzz.build import *
from pyzzz.dmg import *
from pyzzz.model import *


def search(combo: Combo, b: Build, by_index, deep: int, result: list):

    if deep > 6:
        return

    pass


def search(combo: Combo, b: Build, all: list[Disc]):

    by_index = [[], [], [], [], [], [], []]
    for d in all:
        by_index[d.index].append(d)

    candidate = DiscGroup()

    search(Combo)
