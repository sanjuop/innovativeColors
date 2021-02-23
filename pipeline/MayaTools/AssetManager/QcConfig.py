import os
import re
import struct
import imghdr


import pymel.core as pm

import pipeline.MayaTools.maya_wrappers as maya_wrappers;reload(maya_wrappers)
import pipeline.CoreModules.common.common_utils as common_utils;reload(common_utils)

assets_path = common_utils.assets_path

def error_dict(error_message):
    return {"error_message":error_message}

def check_file_name():
    all_files = os.listdir(assets_path)
    file_name = maya_wrappers.getBaseName()
    if file_name not in all_files:
        return error_dict("Assets list in server does not have this file name")
    return True


def check_for_multiple_group():
    all_assemblies = maya_wrappers.get_assembly_nodes()
    if len(all_assemblies) != 1:
        return error_dict("More than one group or no group present in outliner, delete unwanted")
    return True

def rename_hierarchy():

    mul_grp = check_for_multiple_group()
    if mul_grp != True:
        return mul_grp

    file_name = maya_wrappers.getBaseName()
    try:
        main_node = maya_wrappers.get_assembly_nodes()[0]
    except IndexError:
        return error_dict("No Group present in outliner")
    dummy_name = "A"+str(file_name)
    main_node.rename(dummy_name)
    hierarchy_list = []
    def get_children(node):
        for i in node.getChildren(type="transform"):
            hierarchy_list.append(i)
            get_children(i)
    get_children(main_node)
    cnt = 0
    for each_node in hierarchy_list:
        pm.rename(each_node, "%s_%s"%(dummy_name, cnt))
        cnt += 1
    return True

def unfrozenTransforms():
    all_mesh = [i.getTransform() for i in pm.ls(type="mesh")] 
    unfrozenTransforms = []
    for obj in all_mesh:
        translation = pm.xform(obj, q=True, worldSpace=True, translation=True)
        rotation = pm.xform(obj, q=True, worldSpace=True, rotation=True)
        scale = pm.xform(obj, q=True, worldSpace=True, scale=True)
        if not translation == [0.0, 0.0, 0.0] or not rotation == [0.0, 0.0, 0.0] or not scale == [1.0, 1.0, 1.0]:
            unfrozenTransforms.append(obj)
    if unfrozenTransforms:
        all_meshes = [i.name() for i in unfrozenTransforms]
        return error_dict("{} these meshes are unfrozen".format(all_meshes))
    return True

def triangles():
    all_mesh = [i.getTransform() for i in pm.ls(type="mesh")]
    if all_mesh:
        pm.select(all_mesh)
        pm.mel.polyCleanupArgList(3, ["0","2","1","1","1","0","0","0","0","1e-05","0","1e-05","0","1e-05","0","-1","0" ])
        pm.mel.invertSelection()
        if pm.ls(sl=True):
            return error_dict("triangles found\nExecute this QC seperately to find the mesh")
        return True
    return True


def getBuildOrder(face):
    """Returns the uvs of a face in the build order """
    verts = []
    vtxFaces = pm.ls(pm.polyListComponentConversion(face, toVertexFace=True), flatten=True)
    for vtxFace in vtxFaces:
        uvs = pm.polyListComponentConversion(vtxFace, fromVertexFace=True, toUV=True)
        verts.append(uvs[0])
    return verts


def delete_unwanted_nodes():
    maya_wrappers.delete_unused_nodes()
    return True
 
def getUVFaceNormal(face):
    """Returns the UV normals from face"""
    uvs = getBuildOrder(face)
    #print ("uvs are : " + str(uvs))
    #ignore non-valid faces
    if len(uvs) < 3:
        return 1, 0, 0
    #get uvs positions:
    uvA_xyz = pm.polyEditUV(uvs[0], query=True, uValue=True, vValue=True)
    uvB_xyz = pm.polyEditUV(uvs[1], query=True, uValue=True, vValue=True)
    uvC_xyz = pm.polyEditUV(uvs[2], query=True, uValue=True, vValue=True)
    #print uvA_xyz, uvB_xyz, uvC_xyz
    #get edge vector
    uvAB = pm.dt.Vector([uvB_xyz[0]-uvA_xyz[0], uvB_xyz[1]-uvA_xyz[1], 0])
    uvBC = pm.dt.Vector([uvC_xyz[0]-uvB_xyz[0], uvC_xyz[1]-uvB_xyz[1], 0])
    #cross product & normalize
    uvNormal = uvAB.cross(uvBC)
    uvNormal = uvNormal.normal()
    return uvNormal
 
def findReversed(obj):
 	"""Returns meshes with normals pointing inward"""
 	reversed = []
 
 	#Convert to faces, then to vertexFaces:
 	faces = pm.polyListComponentConversion(obj, toFace=True)
 	faces = pm.ls(faces, flatten=True)
 	for face in faces:
 		uv_normal = getUVFaceNormal(face)
 		#print ("uvNormal: " + str(uv_normal))
 		#if the uv face normal is facing into screen then its reversed - add it to the list
 		if (uv_normal * pm.dt.Vector([0, 0, 1])) < 0:
 			reversed.append(face)
 	return reversed

def reverse_mesh_normals():
    all_mesh = [i.getTransform() for i in pm.ls(type="mesh")]
    reversed_meshes = []
    for object in all_mesh:
        #Conform object before looking for reversed faces:
        pm.polyNormal(object, normalMode=2, userNormalMode=0,  ch=1)
        reversed = findReversed(object)
        if reversed:
            reversed_meshes.append(object)
    if reversed_meshes:
        mesh_names = [i.name() for i in reversed_meshes]
        return error_dict("Following meshes normals are not proper:\n{}".format(mesh_names))
    return True


def check_for_jpg():
    non_jpeg_images = {}
    file_nodes = maya_wrappers.get_file_nodes()
    if file_nodes:
        for each_file_node in file_nodes:
            if not re.search("\.jpeg$|\.jpg", file_nodes[each_file_node]):
                non_jpeg_images[each_file_node.name()] = each_file_node.ftn.get()
    if non_jpeg_images:
        return error_dict("non jpg images are present in the scene:\n{}".format(non_jpeg_images))
    return True


def scene_uv_bounds(target = (0,0,1,1)):
    umin, vmin, umax, vmax  = 0, 0, 0, 0
    out_of_bounds = []
    for item in pm.ls(type='mesh'):
        # polyEvaluate -b2 returns [(umin, umax) , (vmin, vmas)]
        uvals, vvals = pm.polyEvaluate(item, b2=True)
        #unpack into separate values
        uumin, uumax = uvals
        vvmin, vvmax = vvals

        if uumin < target[0] or vvmin < target[1] or uumax > target[2] or vvmax > target[3]:
            out_of_bounds.append(item)

        umin = min(umin, uumin)
        umax = max(umax, uumax)
        vmin = min(vmin, vvmin)
        vmax = max(vmax, vvmax)

    if out_of_bounds:
        return error_dict("following nodes have UV's outside the layout:\n{}".format(out_of_bounds))
    return True

def multiple_uv_sets():
    meshes = pm.ls(type='mesh', long=True)
    invalid = []
    for mesh in meshes:
        uvSets = pm.polyUVSet(mesh, query=True, allUVSets=True)
        if len(uvSets) != 1:
            invalid.append(mesh)
    if invalid:
        return error_dict("following meshes have multiple UV's:\n{}".format(invalid))
    return True


def get_image_size(fname):
    '''Determine the image type of fhandle and return its size.
    from draco'''
    with open(fname, 'rb') as fhandle:
        head = fhandle.read(24)
        if len(head) != 24:
            return
        if imghdr.what(fname) == 'png':
            check = struct.unpack('>i', head[4:8])[0]
            if check != 0x0d0a1a0a:
                return
            width, height = struct.unpack('>ii', head[16:24])
        elif imghdr.what(fname) == 'gif':
            width, height = struct.unpack('<HH', head[6:10])
        elif imghdr.what(fname) == 'jpeg':
            try:
                fhandle.seek(0) # Read 0xff next
                size = 2
                ftype = 0
                while not 0xc0 <= ftype <= 0xcf:
                    fhandle.seek(size, 1)
                    byte = fhandle.read(1)
                    while ord(byte) == 0xff:
                        byte = fhandle.read(1)
                    ftype = ord(byte)
                    size = struct.unpack('>H', fhandle.read(2))[0] - 2
                # We are at a SOFn block
                fhandle.seek(1, 1)  # Skip `precision' byte.
                height, width = struct.unpack('>HH', fhandle.read(4))
            except Exception: #IGNORE:W0703
                return
        else:
            return
        return width, height
        
def image_size():
    non_4k_images = []
    file_nodes = maya_wrappers.get_file_nodes()
    if not file_nodes:
        return True
    for each_file in file_nodes:
        image = file_nodes[each_file]
        width, height = get_image_size(image)
        if width != 3840 or height != 2160:
            non_4k_images.append(image)
    
    if non_4k_images:
        return error_dict("following images are not in 4K:\n{}".format(non_4k_images))
    return True

def delete_lights():
    pm.delete([i.getTransform() for i in pm.ls(type=["light"] + pm.listNodeTypes("light"), dag=True)])
    return True


# modeling_qc_list = ["check_file_name", "check_for_multiple_group", "delete_unwanted_nodes", "reverse_mesh_normals", "unfrozenTransforms", "rename_hierarchy", "triangles", "delete_lights"]
modeling_qc_list = ["check_file_name", "check_for_multiple_group", "delete_unwanted_nodes", "reverse_mesh_normals", "unfrozenTransforms", "rename_hierarchy", "delete_lights"]
texturing_qc_list = ["check_for_jpg", "scene_uv_bounds", "image_size", "multiple_uv_sets"]+modeling_qc_list
