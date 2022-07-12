__author___ = "samu.karli"
__version__ = "2022.07.01"

"""
	selection:				Objects to have bounding boxes, tree access
	epsilon:				If difference is smaller than this; optimization ends;							default: 0.001
	isBoundaryOpt:			If True, optimize Perimeter for 2D and Area for 3D objects, else Area/Volume;	default: False
	iStepVolume:			Step size for volume;															default: 7
	iStepPlanar:			Step size for planar;															default: 17
	iStepDivider:			Divider;																		default: 4
	iMaxIteration:			Max number of iterations;														default: 1000
	doDrawIterationBoxes:	if True, draws a box for every iteration step									default: False
"""

#----------------------------------------------------------------------------------

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
#from Rhino.import  (Geometry as geo)
from Grasshopper import DataTree as Tree
from Grasshopper.Kernel.Data import GH_Path as Path
from System import Array
import Rhino

result = Tree[object]()

class UnsupportedObjectException(Exception):
	pass

def detect_planar(theseObj, tol):
	objectsPlane = rs.ViewCPlane()
	meshVertices = []
	unsupported_obj = 0
	isPlanar = True

	#Parse the selection for preliminary object-identification --------------
	for thisObj in theseObj:
		if rs.IsCurve(thisObj):
			vertices = rs.CurvePoints(thisObj)
			meshVertices += vertices
		elif rs.IsSurface(thisObj):
			vertices = rs.SurfacePoints(thisObj)
			meshVertices += vertices
		elif rs.IsPolysurface(thisObj):
			try:
				isPlanar = rs.IsSurfacePlanar(thisObj)
			except ValueErrorException:
				isPlanar = False
			if not isPlanar:
				break
			rs.EnableRedraw(False)
			rs.SelectObject(thisObj)
			rs.Command("_SolidPtOn", False)
			vertices = rs.ObjectGripLocations(thisObj)
			meshVertices += vertices
			rs.EnableObjectGrips(thisObj, False)
		elif rs.IsPoint(thisObj): 
			vertices = rs.PointCoordinates(thisObj)
			meshVertices += [vertices]
		elif rs.IsMesh(thisObj): 
			vertices = rs.MeshVertices(thisObj)
			meshVertices += vertices
		#elif Rhino.IsExtrusion(thisObj):
		#	Rhino.EnableRedraw  (False)
		#	Rhino.EnableObjectGrips  (thisObj, True)
		#	vertices = Rhino.SurfacePoints(thisObj)
		#	meshVertices = Rhino.JoinArrays(meshVertices, vertices)
		#	Rhino.EnableObjectGrips  (thisObj, False)
		#elif rs.IsPointCloud(thisObj):
		#	vertices = rs.PointCloudPoints(thisObj)
		#	meshVertices += vertices
		#elif rs.IsText(thisObj):
		#	textPlane = rs.TextObjectPlane(thisObj)
		#	vertices = [textPlane[0], rs.VectorAdd(textplane[1], textplane[0]), Rhino.VectorAdd(textplane[2], textplane[0])]
		#	meshVertices += vertices
		#elif rs.IsLight(thisObj):
		#	lightPlane = rs.RectangularLightPlane(thisObj)
		#	vertices = [lightPlane[0], rs.VectorAdd(lightplane[1], lightplane[0]), Rhino.VectorAdd(lightplane[2], lightplane[0])]
		#	meshVertices += vertices
		#elif rs.IsBlockInstance(thisObj):
		#	objArr = rs.BlockObjects(Rhino.BlockInstanceId(thisObj))
		#	isBlockPlanar = detect_planar(objArr, tol) #Recursion
		#	if isBlockPlanar[0] < 0:
		#		unsupported_obj = unsupported_obj + 1
		#	if isBlockPlanar[0] == 0:
		#	   isPlanar = False
		#	#Get the origin and x and y vertices of the plane that this planar block is on
		#	#Vertices need to be in world coordinates before going into the meshVertices array
		#	blockXform = Rhino.BlockInstanceXform(thisObj)
		#	temp_plane = Rhino.PlaneTransform(isBlockPlanar[1], blockXform) #origin in world coordinates
		#	vertices = [temp_plane[0], Rhino.VectorAdd(temp_plane[1], temp_plane[0]), Rhino.VectorAdd(temp_plane[2], temp_plane[0])]
		#	meshVertices = Rhino.JoinArrays(meshVertices, vertices)
		#else:
		#	break
	if isPlanar and rs.PointsAreCoplanar(meshVertices):
		objectsPlane = rs.PlaneFitFromPoints(meshVertices)
		return True, objectsPlane
	else:
		return False, rs.ViewCPlane()

iBranch = selection.BranchCount

for i in range(iBranch):
	branch = selection.Branch(i)
	patternPath = selection.Path(i)
	
	#--Default values--
	absTolerance =	Rhino.RhinoDoc.ActiveDoc.ModelAbsoluteTolerance
	DefaultTolerance = 0.1
	fStart = Rhino.Geometry.Vector3d(0, 0, 0)											#XY, XZ, YZ - In Degrees
	fEnd = Rhino.Geometry.Vector3d(90, 90, 90)											#In Degrees
	loopStep = Rhino.Geometry.Vector3d.Subtract(fEnd, fStart)							#LoopStep starts as the whole range
	iteration = 0
	ThisView = rs.CurrentView()															#String
	thiscplane = rs.ViewCPlane()
	thisCplaneName = "Temp**MinBoundBox3d^^1"
	rs.scriptcontext.doc = Rhino.RhinoDoc.ActiveDoc
	rs.AddNamedCPlane(thisCplaneName, ThisView)

	isPlanar, detectedPlane = detect_planar(branch, absTolerance)
	
	#--Main script
	rs.EnableRedraw(False)
	#print("Please wait (Brute-force calculation may take a few minutes)")
	if isPlanar:
		startingCplane = detectedPlane													#Contents of ViewCplane from Detect_Planar function
		loopStep = Rhino.Geometry.Vector3d.Divide(loopStep, iStepPlanar)				#Initial LoopStep size
	else:
		startingCplane = thiscplane
		loopStep = Rhino.Geometry.Vector3d.Divide(loopStep, iStepVolume)				#Initial LoopStep size

	while True:
		aYZ = fStart[2]
		while aYZ < fEnd[2]:
			aXZ = fStart[1]
			while aXZ < fEnd[1]:
				aXY = fStart[0]
				while aXY < fEnd[0]:
					iteration += 1

					#calculate cPlane rotation
					if isPlanar:
						tempCplane = rs.RotatePlane(startingCplane, aXY, startingCplane.ZAxis)
					else:
						tempCplane = rs.RotatePlane(startingCplane, aYZ, startingCplane[1])
						tempCplane = rs.RotatePlane(tempCplane, aXZ, tempCplane[2])
						tempCplane = rs.RotatePlane(tempCplane, aXY, tempCplane[3])
					rs.ViewCPlane(ThisView, tempCplane)									#commit the rotation

					#--Bounding box for this iteration
					_sG = [str(g) for g in branch]
					tempBox = rs.BoundingBox(_sG, ThisView, True)						#cPlane aligned, but using world coordinates

					xSpan = rs.VectorLength(rs.VectorSubtract(tempBox[1], tempBox[0]))
					ySpan = rs.VectorLength(rs.VectorSubtract(tempBox[3], tempBox[0]))
					zSpan = rs.VectorLength(rs.VectorSubtract(tempBox[4], tempBox[0]))

					#Metric to be minimized over time
					if not isPlanar and		isBoundaryOpt: boxMetric_now = 2 * xSpan * ySpan + 2 * xSpan * zSpan + 2 * ySpan * zSpan	#Area
					if not isPlanar and not isBoundaryOpt: boxMetric_now = xSpan * ySpan * zSpan										#Volume

					if isPlanar and		isBoundaryOpt: boxMetric_now = 2 * xSpan + 2 * ySpan											#Perimeter
					if isPlanar and not isBoundaryOpt: boxMetric_now = xSpan * ySpan													#Area

					#error detect
					if (xSpan < epsilon or ySpan < epsilon or zSpan < epsilon) and not isPlanar:
						rs.RestoreNamedCPlane(thisCplaneName, ThisView)
						rs.DeleteNamedCPlane(thisCplaneName)
						rs.EnableRedraw(True)
						print "Script unsuccessful (Improper attempt for min volume Box calculation on planar object(s) )"

					#-Run this ONCE EVER
					if iteration == 1:
						boxMetric_epsilon = epsilon
						boxMetric_min = boxMetric_now									#Initial value for min is the first box itself
						boxMetric_delta = boxMetric_epsilon / 2							#In case the original box is the smallest one already
				
						bbox_min = tempBox
						angle_min = Rhino.Geometry.Vector3d(aXY, aXZ, aYZ)
		
					#-Run this ONCE at the beginning of EVERY PARSING -
					if aXY == fStart[0] and aXZ == fStart[1] and aYZ == fStart[2]:
						boxMetric_start = boxMetric_min									#boxMetric_start is the known min at the beginning of this parsing
		
					#DETECT MIMIMUM ---------------------------------------------------
					if boxMetric_now < boxMetric_min:
						#--Found new minimum
						boxMetric_delta = boxMetric_start - boxMetric_now				#The difference between the min box and the starting box from the beginning of this parsing
						boxMetric_min = boxMetric_now
						if doDrawIterationBoxes:
							rs.AddBox(tempBox)
						bbox_min = tempBox												#This is the box to be drawn on screen
						angle_min = Rhino.Geometry.Vector3d(aXY, aXZ, aYZ)
					aXY += loopStep[0]
				if isPlanar:
					break
				aXZ += loopStep[1]
			if isPlanar:
				break
			aYZ += loopStep[2]
		percent = boxMetric_epsilon / boxMetric_delta

		if percent > 1:
			percent = 1
	
		#--Tighten the loop parameters
		#--There is an issue in that this method might be getting stuck into local minima
		if boxMetric_delta > boxMetric_epsilon and iteration < iMaxIteration:
			#set cplane to rotate again

			#New start and end ranges for the for loops
			fStart = rs.VectorSubtract(angle_min, loopStep)
			fEnd = rs.VectorAdd(angle_min, loopStep)
			loopStep = rs.VectorDivide(loopStep, iStepDivider) #adjust step increment
		else:
			break

	#--Draw the minimum found bounding box
	if not isPlanar:																							#3D box
		result.Add(Rhino.Geometry.Box(Rhino.Geometry.Plane(bbox_min[0], bbox_min[1], bbox_min[3]), bbox_min))
	else:																										#Perimeter box
		result.Add(Rhino.Geometry.Polyline([bbox_min[0], bbox_min[1], bbox_min[2], bbox_min[3], bbox_min[0]]))
	
	#--Reset to original cplane
	rs.RestoreNamedCPlane(thisCplaneName, ThisView)
	rs.DeleteNamedCPlane(thisCplaneName)
	rs.EnableRedraw(True)

