import os
import string
import random
import logging
import shutil
import glob
import re

import maya.mel as mel
import maya.OpenMayaUI as omui
import maya.cmds as cmds
import pymel.core as pm

import config as config;reload(config)
import dialogue as dialogue;reload(dialogue)
import maya_wrapper as maya_wrapper;reload(maya_wrapper)
import utility as utility;reload(utility)


def define_interaction_mesh():
    selected_meshes = [i for i in pm.ls(sl=1) if i.getShape().hasAttr("displaySubdComps")]
    if pm.objExists(config.int_set):
        if dialogue.warning("warning", config.int_set, "interaction meshes exists\nDo you want to redefine it"):
            pm.delete(config.int_set)
            pm.sets(selected_meshes, n=config.int_set)
    else:
        pm.sets(selected_meshes, n=config.int_set)
        

def export_interaction_meshes(dir_path=None):
    if pm.objExists(config.int_set):
        int_mesh_set = pm.PyNode(config.int_set)
        meshes = int_mesh_set.members()
        pm.select(meshes)

        # export selected meshes
        if dir_path:
            path_to_export = dir_path
        else:
            path_to_export = os.path.dirname(maya_wrapper.get_scene_name(dir_base=True)[0])
        file_name = "interaction_mesh.ma"
        path_to_export = re.sub("/layout|/animation","/lighting",path_to_export)
        if os.path.exists(os.path.join(path_to_export, file_name)):
            os.remove(os.path.join(path_to_export, file_name))
        pm.exportSelected(os.path.join(path_to_export, file_name))


def get_meshes_from_sets(sets_list):
    meshes = [each_mesh for each_set in sets_list for each_mesh in each_set.members()]
    return meshes


def add_meshes_to_layers(sets_list, layers):
    meshes = get_meshes_from_sets(sets_list)
    for layer in layers:
        pm.editRenderLayerMembers(layer, meshes)


def create_id_json_file(matte_id_path, asset_name, highest_num, data, hnu=True):
    print "matte_id_path",matte_id_path
    new_asset_file = asset_name+".json"
    asset_temp_path = os.path.join(config.maya_temp_path, new_asset_file)
    utility.write_json_file(asset_temp_path, data)
    shutil.copy2(asset_temp_path, matte_id_path)
    os.remove(asset_temp_path)
    if hnu:
        highest_num_file = os.path.join(config.maya_temp_path, "HighestNumber.txt")
        utility.write_text_file(highest_num_file, [str(highest_num+1)])
        shutil.copy2(highest_num_file, matte_id_path)
        os.remove(highest_num_file)


def get_asset_type(assets_hierarchy,namespace):
    for i in assets_hierarchy.keys():
        i_keys = assets_hierarchy[i]
        if i_keys.has_key(namespace):
            return i

def publish_id(all_assets,assets_hierarchy):
    inc_value = 0.0000000001
    highest_num_file = os.path.join(config.matte_id_path, "HighestNumber.txt")
    for each_asset in all_assets.values():
        if "cam" in each_asset.path:
            continue
        highest_num = int(utility.read_text_file(highest_num_file)[0])
        asset_name = each_asset.path.basename().split(".")[0]
        print "asset_name",asset_name
        namespace = each_asset.namespace
        asset_type = get_asset_type(assets_hierarchy,namespace)
        pattern = os.path.join(config.matte_id_path, asset_name+".json")
        file_name = glob.glob(pattern)
        print "pattern",pattern
        meshes = maya_wrapper.get_meshes_from_top_group(each_asset)
        meshes = [mesh.split(":")[1] for mesh in meshes]
        if not file_name:
            print "@95", meshes
            id_data = {"RID": highest_num}
            oid_value = highest_num + inc_value
            for eachMesh in meshes:
                id_data[eachMesh] = round(oid_value, 10)
                oid_value += inc_value
                create_id_json_file(config.matte_id_path, asset_name, highest_num, id_data, hnu=True)
                file_name = [os.path.join(config.matte_id_path, asset_name + ".json")]

        print "file_name",file_name
        iddata = utility.read_json_file(str(file_name[0]))
        highest_oid_num = max(iddata.values()) + inc_value
        for eachEx in meshes:
            if not iddata.has_key(eachEx):
                iddata[eachEx] = highest_oid_num
                highest_oid_num += inc_value
                create_id_json_file(config.matte_id_path, asset_name, highest_num, iddata, hnu=False)
        rid = iddata["RID"]
        pm.PyNode(namespace + "_" + asset_type + "_rsObjectId").attr("objectId").set(rid)
        for eachData in iddata:
            mesh_name = each_asset.namespace + ":" + eachData
            if pm.objExists(mesh_name):
                oid = iddata[eachData]
                trans_node = pm.PyNode(mesh_name)
                maya_wrapper.add_custom_attr(trans_node, oid, "OID")

