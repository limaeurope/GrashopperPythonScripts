__author__ = "samu.karli"
__version__ = "2022.04.27"

hor__ = "samu.karli"
__version__ = "2022.04.27"


if isTest:
    import ptvsd

    if not ptvsd.is_attached():
        try:
            ptvsd.enable_attach(secret = 'dev', address = ('localhost', 2019))
        except:
            pass

        ptvsd.wait_for_attach()

#----------------------------------------------------------------------------------

epsilon = 0.01

from Rhino import Geometry
import sys
import pprint
from Grasshopper import DataTree as Tree


def isNotVertical(p_):
    return not p_.NormalAt(0,0).IsParallelTo(Geometry.Vector3d(0,0,1)) in {1,-1}

List = Tree[object]()

for i in range(surf.BranchCount):
    branchList = surf.Branch(i)
    branchPath = surf.Path(i)

    zBottom = sys.float_info.max

    for brep in branchList:
        try:
            item = brep.Surfaces[0]
            if isinstance(item, Geometry.Surface):
                zBottom = min(zBottom, Geometry.AreaMassProperties.Compute(item).Centroid.Z)
        except (TypeError, AttributeError):
            continue
    
    for brep in branchList:
        try:
            item = brep.Surfaces[0]
            if isinstance(item, Geometry.Surface) and \
            (Geometry.AreaMassProperties.Compute(item).Centroid.Z > zBottom + epsilon or isNotVertical(item)):
                List.Add(item, branchPath)
        except (TypeError, AttributeError):
            continue

