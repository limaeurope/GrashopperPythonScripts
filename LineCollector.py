__author__ = "samu.karli"
__version__ = "2022.12.09"

import rhinoscriptsyntax as rs						# For direct Rhino commands
import Rhino
from Grasshopper import DataTree as Tree
from Grasshopper.Kernel.Data import GH_Path as Path
from System import Array
import scriptcontext as sc
import ghpythonlib.components as ghcomp				# Grasshopper's components are available through this

import httplib
import json
from  urllib import urlencode


if isTest:
    import ptvsd

    if not ptvsd.is_attached():
        try:
            ptvsd.enable_attach(secret = 'dev', address = ('localhost', 2019))
        except:
            pass

        ptvsd.wait_for_attach()


iBranch = pointTree.BranchCount

postData = {'points': []}

for i in range(iBranch):
    points = pointTree.Branch(i)      #list

    for point in points:
        postData['points'].append([point.X, point.Y])

postData['xEPS'] = EPS
postData['aEPS'] = AngularEPS

try:
    h1 = httplib.HTTPConnection('localhost:1975', timeout=30)

    h1.connect()
    headers = {}
    h1.request('POST', 'localhost:1975', json.dumps(postData), headers )
    _result = h1.getresponse().read()
    j = json.loads(_result)
    
    i = 0
    result = Tree[object]()
    for p in j["resultPoints"]:
        path = Path(Array[int]([0, i]))
        #result.Add(Rhino.Geometry.Point(p[0], p[1], 0), path)
        result.Add(Rhino.Geometry.Point3d(p[0], p[1], 0), path)
        i += 1
except:
    pass

