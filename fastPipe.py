import maya.cmds as cmds

def run(radius, sides):
	cmds.undoInfo(openChunk=True)

	edgeloop = cmds.ls(selection= True)
	pipeCurve = makeCurve(edgeloop)
	circle = makeCircle(radius, sides)
	makePipe(circle, pipeCurve)

	cmds.undoInfo(closeChunk=True)

def makeCircle(radius, sides):
	return cmds.circle(radius=radius, sections=sides, degree=1, normal=(0,1,0))

def makeCurve(edgeloop):
	return cmds.polyToCurve(form=2, degree=1)

def makePipe(circle, pipeCurve):
	pipeSweep = sweepPipe(circle, pipeCurve)
	nurbsPipe = cmds.loft(pipeSweep, degree=1, reverseSurfaceNormals=True)
	polyPipe = cmds.nurbsToPoly(nurbsPipe[0], name="fastPipe", format=3, matchNormalDir=True, polygonType=1)
	cmds.polyMergeVertex(polyPipe[0], d=0.1, alwaysMergeTwoVertices=True)
	# cmds.delete(pipeSweep, nurbsPipe, circle, pipeCurve, constructionHistory=True)
	cmds.delete(pipeSweep[0], nurbsPipe[0], circle[0], pipeCurve[0])
	cmds.select(polyPipe)

def sweepPipe(circle, pipeCurve):
	numberOfCVs = cmds.getAttr('%s.cp' % pipeCurve[0], size=1)
	motionPath = cmds.pathAnimation("%s" % circle[0], curve=pipeCurve[0], follow=True, startTimeU=1, endTimeU=numberOfCVs)
	cmds.selectKey("%s.uValue" % motionPath)
	cmds.keyTangent( itt="linear", ott="linear")
	pipeSweep = cmds.snapshot(circle, startTime=1, endTime=numberOfCVs)
	return pipeSweep