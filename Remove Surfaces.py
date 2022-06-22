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

epsilon = 0.01

from Rhino import Geometry
from Rhino import RhinoMath
import sys
import pprint
from Grasshopper import DataTree as Tree

def isNotVertical(p_surface, p_aMax):
    _angle = RhinoMath.ToDegrees(Geometry.Vector3d.VectorAngle(p_surface.NormalAt(0,0), Geometry.Vector3d(0,0,1)))
    return _angle > p_aMax

List = Tree[object]()

for i in range(surf.BranchCount):
    branchList = surf.Branch(i)
    branchPath = surf.Path(i)

    zExt = -sys.float_info.max if isTop else sys.float_info.max
    fExt = max if isTop else min
    fCriterium = lambda z : z < zExt - epsilon if isTop else z > zExt + epsilon

    for brep in branchList:
        try:
            item = brep.Surfaces[0]
            zExt = fExt(zExt, Geometry.AreaMassProperties.Compute(item).Centroid.Z)
            zExt = fExt(zExt, *[p.Z for p in item.Points])
        except (TypeError, AttributeError):
            continue
    
    for brep in branchList:
        try:
            if isinstance(brep, Geometry.Brep):
                item = brep.Surfaces[0]
                #if fCriterium(Geometry.AreaMassProperties.Compute(item).Centroid.Z) or isNotVertical(item, aMax):
                if fCriterium(fExt([p.Z for p in item.Points])) or isNotVertical(item, aMax):
                    List.Add(brep, branchPath)
        except (TypeError, AttributeError):
            continue

