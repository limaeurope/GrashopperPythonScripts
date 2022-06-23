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

##----------------------------------------------------------------------------------

epsilon = 0.01

import rhinoscriptsyntax as rs
from Rhino import Geometry as geo
from Grasshopper import DataTree as Tree
from Grasshopper.Kernel.Data import GH_Path as Path
from System import Array
from math import sqrt
from collections import deque

List = Tree[object]()
iBranch = windows.BranchCount
resultDict = {}


class counterDict():
    def __init__(self, zWall):
        self.dict = {}
        self.zWall = int(zWall)

    def inc(self, key, inc=1):
        if key not in self.dict:
            self.dict[key] = 0
        self.dict[key] += inc

    def dec(self, key, dec=1):
        if key in self.dict:
            self.dict[key] -= dec
            if self.dict[key] == 0:
                del self.dict[key]

    def calcLength(self):
        self.dec(self.zWall, 2)
        return self.dict.keys()[0]

    def returnSizes():
        if self.dict.keys[0] == 4:
            return (self.dict.keys()[0], self.dict.keys()[0])
        else:
            return (self.dict.keys()[1], self.dict.keys()[0])


for i in range(iBranch):
    breps = windows.Branch(i)      #list
    branchPath = windows.Path(i)
    path = Path(Array[int]([0, i]))
    _zWall = zWall.Branch(i)[0]
    _dists=counterDict(_zWall)

    for face in breps:
        _2 = list(face.Points)
        point2 = [_2[1], _2[3], _2[0], _2[2], ]
        _points = counterDict(_zWall)

        for point1, point2 in zip(face.Points, point2):
            dX = point1.X - point2.X
            dY = point1.Y - point2.Y
            dZ = point1.Z - point2.Z
            _dist = sqrt(dX ** 2 + dY ** 2 + dZ ** 2)
            _points.inc(round(_dist, 0))

        _dist = int(_points.calcLength())
        _dists.inc(_dist)

    if _dists.dict:
        sizes = sorted(_dists.dict.keys())
        _zW = int(round(_zWall, 0))
        sizesTuple = (sizes[0], sizes[-1], _zW)
        resultDict[sizesTuple] = resultDict[sizesTuple] + 1 if sizesTuple in resultDict else 1

path = Path(Array[int]([0]))

for k, v in resultDict.iteritems():
    List.Add(str(k[0]) + u"\u00D7" + str(k[1]) + u" (\u00D7" + str(k[2]) + ")" + ": " + str(v), path)