import os
import re
import pymel.core as pm

import pipeline.MayaTools.maya_wrappers as maya_wrappers;reload(maya_wrappers)
import pipeline.CoreModules.common_utils as common_utils;reload(common_utils)

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


def check_for_jpg():
    non_jpeg_images = {}
    file_nodes = maya_wrappers.get_file_nodes()
    if file_nodes:
        for each_file_node in file_nodes:
            if re.search("\.jpeg$|\.jpg", each_file_node):
                non_jpeg_images[each_file_node.name()] = each_file_node.fnt.get()
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

def multiple_uv_sets(self, instance):
    meshes = pm.ls(instance, type='mesh', long=True)
    invalid = []
    for mesh in meshes:
        uvSets = pm.polyUVSet(mesh, query=True, allUVSets=True)
        if len(uvSets) != 1:
            invalid.append(mesh)
    if invalid:
        return error_dict("following nodes have UV's outside the layout:\n{}".format(invalid))
    return True
    


modeling_qc_list = ["check_file_name", "check_for_multiple_group", "unfrozenTransforms", "rename_hierarchy", "triangles"]
texturing_qc_list = ["check_for_jpg"]+modeling_qc_list


     