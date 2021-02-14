import os

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
    print "check_for_jpg"
    return True


modeling_qc_list = ["check_file_name", "check_for_multiple_group", "unfrozenTransforms", "rename_hierarchy", "triangles"]
texturing_qc_list = ["check_for_jpg"]+modeling_qc_list


     