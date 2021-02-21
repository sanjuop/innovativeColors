import maya.cmds as mc
ignoreNodes = 'defaultColorMgtGlobals'

def getUpstreamNodes(root):

	MAX_SEARCH_LEVEL = 50

	allNodes = []
	conectedNodes=[]

	nextLevel = [root]

	for l in range(0, MAX_SEARCH_LEVEL):

		if len(nextLevel) == 0:
			break
		
		for i in nextLevel:

			try:
				nextLevel.remove(i)
			except ValueError:
				pass

			conectedNodes = mc.listConnections(i, sh=True, s=True, d=False)
			try:
				conectedNodes = list(set(conectedNodes))
				nextLevel += conectedNodes
	
			except:
				continue
                        
			allNodes += conectedNodes
			
			nextLevel = list(set(nextLevel))

		conectedNodes=[]
	
	if ignoreNodes in allNodes:
		allNodes.remove(ignoreNodes)
	
	return allNodes


#allNodes = getUpstreamNodes("UHAUL_metal_A_shad")