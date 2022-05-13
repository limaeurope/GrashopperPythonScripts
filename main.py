import ptvsd

if not ptvsd.is_attached():
    try:
        ptvsd.enable_attach(secret = 'dev', address = ('localhost', 2019))
    except:
        pass

    ptvsd.wait_for_attach()


print("OK")

#__author__ = "samu.karli"
#__version__ = "2022.04.27"

#epsilon = 0.01

#import rhinoscriptsyntax as rs
#from scriptcontext import sticky
#from Rhino import Geometry
#import sys
#import pprint
#from types import NoneType
#import ghpythonlib.treehelpers as th

#_surf = th.tree_to_list(surf)
#pprint.pprint(_surf)


#def isNotVertical(p_):
#    return not p_.NormalAt(0, 0).IsParallelTo(Geometry.Vector3d(0, 0, 1)) in {1, -1}


#def isSurface(p_):
#    return isinstance(p_, Geometry.Surface) or isinstance(p_, NoneType)


#def isTree(p_branch):
#    if all(map(lambda file: isinstance(file, list) or isinstance(file, NoneType), p_branch)):
#        print()
#        return True


#def removeTopSurfaces(p_branch):
#    if isinstance(p_branch, list):
#        if not isTree(p_branch):
#            # List
#            if all(map(isSurface, p_branch)):
#                zTop = -sys.float_info.max

#                for item in p_branch:
#                    if isinstance(item, Geometry.Surface):
#                        zTop = max(zTop, Geometry.AreaMassProperties.Compute(item).Centroid.Z)

#                p_branch = [s for s in p_branch if
#                            isinstance(s, Geometry.Surface) and
#                            (Geometry.AreaMassProperties.Compute(s).Centroid.Z < zTop - epsilon or isNotVertical(s))
#                            ].sort(key=lambda s: Geometry.AreaMassProperties.Compute(s).Centroid.Z)
#        else:
#            # Tree
#            p_branch = map(removeTopSurfaces, p_branch)
#    else:
#        if isinstance(p_branch, NoneType):
#            return []
#        else:
#            return p_branch

#    return p_branch


#_ = removeTopSurfaces(_surf)

#pprint.pprint(_)

#List = th.list_to_tree(_)

