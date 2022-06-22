__author___ = "samu.karli"
__version__ = "2022.04.27"


#if isTest:
#    import ptvsd

#    if not ptvsd.is_attached():
#        try:
#            ptvsd.enable_attach(secret = 'dev', address = ('localhost', 2019))
#        except:
#            pass

#        ptvsd.wait_for_attach(10)

#----------------------------------------------------------------------------------


import rhinoscriptsyntax as rs
from Rhino import Geometry as geo
from Grasshopper import DataTree as Tree
from Grasshopper.Kernel.Data import GH_Path as Path
from System import Array


class PathAsList():
    def __init__(self, p_enumerable):
        self._list = p_enumerable

    def __lt__(self, y):
        for this, that in zip(self._list, y._list):
            if this < that:
                return True
        return False


lData = []
iData = data.BranchCount
for i in range(iData):
    lData.append((data.Path(i), data.Branch(i)[0]))

result = Tree[object]()

dataIterator = iter(lData)
_d = next(dataIterator)
dataPath = _d[0]
dataData = _d[1]

List = Tree[object]()
iBranch = pattern.BranchCount

for i in range(iBranch):
    branch = pattern.Branch(i)
    patternPath = pattern.Path(i)
    
    while PathAsList(dataPath) < PathAsList(patternPath):
        _d = next(dataIterator)
        dataPath = _d[0]
        dataData = _d[1]
    result.Add(dataData, patternPath)

