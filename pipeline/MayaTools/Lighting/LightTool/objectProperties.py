import pymel.core as pm
import maya.mel as mel


def get_rs_node_type_info():
	rsobjp_cmd = ['redshiftCreateObjectIdNode()',
				'redshiftCreateVisibilityNode()',
				'redshiftCreateMeshParametersNode()',
				'redshiftCreateMatteParametersNode()']
	rsobjp_types = ['RedshiftObjectId',
					'RedshiftVisibility',
					'RedshiftMeshParameters',
					'RedshiftMatteParameters']
	rsobjp_short = ['rsObjectId',
					'rsVisibility',
					'rsMeshParameters',
					'rsMatteParameters']
	rsobjp_enable= ['enable',
					'enable',
					'enableSubdivision',
					'matteEnable']
	return [rsobjp_cmd,rsobjp_types,rsobjp_short, rsobjp_enable]


def create_rs_obj_pro_node_process(type, nmspc, enable=1):
	"""
	type=0,1,2,3
	"""
	rsObjP_Cmd    = get_rs_node_type_info()[0]
	rsObjP_Types  = get_rs_node_type_info()[1]
	rsObjP_Short  = get_rs_node_type_info()[2]
	rsObjP_Enable = get_rs_node_type_info()[3]
	
	rsNode = mel.eval(rsObjP_Cmd[type])
	
	rsNodeName = '%s_%s'%(nmspc, rsObjP_Short[type])
	pm.rename(rsNode, '%s_%s'%(nmspc,rsObjP_Short[type]))
	
	pm.setAttr("%s.%s"%(rsNodeName,rsObjP_Enable[type]), enable)
	pm.select(cl=1)
	return rsNodeName
	
	
def create_rs_obj_pro_node(type, nmspc, meshes, enable=1):
	pm.select(meshes, r=1)
	rsnodename = pm.PyNode(create_rs_obj_pro_node_process(type, nmspc, enable))
	return rsnodename


def get_rs_obj_pro_node(NodetType, assetType):
	if NodetType == 0:
		if assetType == "BG":
			BG_rsObjectId = pm.ls("*_BG_rsObectId", type="RedshiftObjectId")
			return BG_rsObjectId
		elif assetType == "CHAR":
			CH_rsObjectId = pm.ls("*_CHAR_rsObjectId", type="RedshiftObjectId")
			return CH_rsObjectId
	if NodetType == 1:
		if assetType == "BG":
			BG_rsVisibility = pm.ls('*_BG_rsVisibility', type="RedshiftVisibility")
			return BG_rsVisibility
		elif assetType == "CHAR":
			CH_rsVisibility = pm.ls('*_CHAR_rsVisibility', type="RedshiftVisibility")
			return CH_rsVisibility
	if NodetType == 2:
		if assetType == "BG":
			BG_rsMeshParameters = pm.ls('*_BG_rsMeshParameters', type="RedshiftMeshParameters")
			return BG_rsMeshParameters
		elif assetType == "CHAR":
			CH_rsMeshParameters = pm.ls("*_CHAR_rsMeshParameters", type="RedshiftMeshParameters")
			return CH_rsMeshParameters
	if NodetType == 3:
		if assetType == "BG":
			BG_rsMatteParameters = pm.ls('*_BG_rsMatteParameters', type="RedshiftMatteParameters")
			return BG_rsMatteParameters
		elif assetType == "CHAR":
			CH_rsMatteParameters = pm.ls("*_CHAR_rsMatteParameters", type="RedshiftMatteParameters")
			return CH_rsMatteParameters