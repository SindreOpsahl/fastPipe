#to use:
#import fastPipe
#fastPipe.run(thickness value, radial subdivisions)

import maya.cmds as cmds

#main proc, call this when running the script.
def run(radius, sides):
	cmds.undoInfo(openChunk=True)

	edgeloop = cmds.ls(selection= True)
	
	pipeCurve = makeCurve(edgeloop)
	circle = makeCircle(radius, sides)
	makePipe(circle, pipeCurve)

	cmds.undoInfo(closeChunk=True)

#proc to create a circle which will define the thickness and divisions of the pipe
def makeCircle(radius, sides):
	return cmds.circle(radius=radius, sections=sides, degree=1, normal=(0,1,0))

#proc to generate a nurbs curve from the edgeloop, which the circle will be lofted along
def makeCurve(edgeloop):
	return cmds.polyToCurve(form=2, degree=1)

#proc to generate the pipe as nurbs, and convert it to a polygon mesh
def makePipe(circle, pipeCurve):
	pipeSweep = sweepPipe(circle, pipeCurve)
	nurbsPipe = cmds.loft(pipeSweep, degree=1, reverseSurfaceNormals=True)
	polyPipe = cmds.nurbsToPoly(nurbsPipe[0], name="fastPipe", format=3, matchNormalDir=True, polygonType=1)
	cmds.polyMergeVertex(polyPipe[0], d=0.1, alwaysMergeTwoVertices=True)
	cmds.delete(pipeSweep[0], nurbsPipe[0], circle[0], pipeCurve[0])
	cmds.select(polyPipe)

#proc to place the circle along the curve
def sweepPipe(circle, pipeCurve):
	numberOfCVs = cmds.getAttr('%s.cp' % pipeCurve[0], size=1)
	motionPath = cmds.pathAnimation("%s" % circle[0], curve=pipeCurve[0], follow=True, startTimeU=1, endTimeU=numberOfCVs)
	cmds.selectKey("%s.uValue" % motionPath)
	cmds.keyTangent( itt="linear", ott="linear")
	pipeSweep = cmds.snapshot(circle, startTime=1, endTime=numberOfCVs)
	return pipeSweep