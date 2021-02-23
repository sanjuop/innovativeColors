import re
import os
import shutil

import pymel.core as pm

import maya_wrapper as maya_wrapper;reload(maya_wrapper)
import dialogue as dialogue;reload(dialogue)
import config as config;reload(config)
import utility as utility;reload(utility)
import lighting_wrapper as lighting_wrapper;reload(lighting_wrapper)
import objectProperties as objectProperties;reload(objectProperties)

ep, seq, shot, shot_name = maya_wrapper.get_scene_details_from_scene_name()
shot_light_path = config.get_shot_path(ep, seq, shot)


def bg_bty():
    # file_name = maya_wrapper.get_scene_name(full_path=True)
    # if file_name == "":
    #     dialogue.message("warning", config.PRJCODE, "Open masterfile and continue the process")
    #     return
    #
    # if not re.search("master", file_name):
    #     dialogue.message("warning", config.PRJCODE, "Its not a master file")
    #     return

    scene_cleanup()

    # import light rig
    light_rig_name = get_shot_wise_light_rig_name()
    light_rig_path = light_rig_name+".ma"

    maya_wrapper.import_scene(light_rig_path)

    bg_layers = pm.ls("BG_*",type="renderLayer")
    bg_sets = pm.ls("*_BG*", et="objectSet")

    lighting_wrapper.add_meshes_to_layers(bg_sets, bg_layers)

    layer_override(os.path.dirname(light_rig_name))
    
    maya_wrapper.update_frame_range()
    
    maya_wrapper.delete_unkown_nodes()

    file_saving(mode = "BG_BTY")

    dialogue.message("message", config.PRJCODE, "BG BTY file successfully created")

def ch_bty():
    # file cleanup
    scene_cleanup()

    #import ch_bty light_layer_setup
    maya_wrapper.import_scene(config.ch_bty_light_layer_setup)

    #import INT lights
    light_rig_name = get_shot_wise_light_rig_name()
    light_rig_path = os.path.join(light_rig_name, light_rig_name + "_INT.ma")
    maya_wrapper.import_scene(light_rig_path)
    pm.editRenderLayerMembers("CH_INT","INT_LIGHTS")

    #add char to char layers
    ch_layers = pm.ls("CH_*", type="renderLayer")
    ch_sets = pm.ls("*_CHAR", et="objectSet")
    lighting_wrapper.add_meshes_to_layers(ch_sets, ch_layers)

    #face mesh holdout matte
    face_layer = "CH_FACE"
    ch_face_layers = pm.ls(face_layer, type="renderLayer")
    ch_face_sets = pm.ls("*_CHAR_face_geos", et="objectSet")
    lighting_wrapper.add_meshes_to_layers(ch_face_sets, ch_face_layers)
    pm.editRenderLayerGlobals(crl = face_layer)
    all_char_matte_vop = objectProperties.get_rs_obj_pro_node(3, "CHAR")
    for each_matte_vop in all_char_matte_vop:
        pm.editRenderLayerAdjustment(each_matte_vop+".matteEnable")
        each_matte_vop.attr("matteEnable").set(1)
        each_matte_vop.attr("matteAlpha").set(0)


    layer_override(os.path.dirname(light_rig_name))
    
    maya_wrapper.update_frame_range()
    
    maya_wrapper.delete_unkown_nodes()
    
    #file saving
    file_saving(mode = "CH_BTY")

    dialogue.message("message", config.PRJCODE, "CH Beauty file successfully created")


def ch_utility():

    scene_cleanup()

    maya_wrapper.import_scene(config.ch_utility)

    ch_layers = pm.ls("CH_*", type="renderLayer")
    ch_sets = pm.ls("*_CHAR", et="objectSet")
    lighting_wrapper.add_meshes_to_layers(ch_sets, ch_layers)

    shadow_layer = "CH_SHD"
    pm.editRenderLayerGlobals(crl = shadow_layer)

    #add shd lights to SHD layer
    light_rig_name = get_shot_wise_light_rig_name()
    light_rig_path = os.path.join(light_rig_name, light_rig_name + "_SHD.ma")
    maya_wrapper.import_scene(light_rig_path)
    pm.editRenderLayerMembers(shadow_layer, "CH_SHD_LIGHTS")

    #add interaction mesh to SHD layer
    interaction_mesh_set = pm.PyNode("interaction_mesh_set")
    lighting_wrapper.add_meshes_to_layers([interaction_mesh_set], [pm.PyNode(shadow_layer)])
    shadow_catcher_mat = pm.PyNode("SHD_CATCHER")
    pm.select(pm.sets("interaction_mesh_set", q=1), r=1)
    pm.hyperShade(a=shadow_catcher_mat)

    # all char visibility off
    all_char_vis_vop = objectProperties.get_rs_obj_pro_node(1, "CHAR")
    for each_vis_vop in all_char_vis_vop:
        pm.editRenderLayerAdjustment(each_vis_vop + ".primaryRayVisible")
        each_vis_vop.attr("primaryRayVisible").set(0)
        
    all_bg_vis_vop = objectProperties.get_rs_obj_pro_node(1, "BG")
    print "all_bg_vis_vop", all_bg_vis_vop
    for all_bg_vis_vop in all_bg_vis_vop:
        pm.editRenderLayerAdjustment(all_bg_vis_vop + ".shadowCaster")
        all_bg_vis_vop.attr("shadowCaster").set(0)
        pm.editRenderLayerAdjustment(all_bg_vis_vop + ".aoCaster")
        all_bg_vis_vop.attr("aoCaster").set(0)
        

    ch_iid_lay = "CH_IID"
    pm.editRenderLayerGlobals(crl = ch_iid_lay)
    all_char_objId_vop = objectProperties.get_rs_obj_pro_node(0, "CHAR")
    for each_ch_oid_vop in all_char_objId_vop:
        pm.editRenderLayerAdjustment(each_ch_oid_vop + ".objectId")
        each_ch_oid_vop.attr("objectId").set(1)

    all_bg_objId_vop = objectProperties.get_rs_obj_pro_node(0, "BG")
    for each_bg_oid_vop in all_bg_objId_vop:
        pm.editRenderLayerAdjustment(each_bg_oid_vop + ".objectId")
        each_bg_oid_vop.attr("objectId").set(0)
    lighting_wrapper.add_meshes_to_layers([interaction_mesh_set], [pm.PyNode(ch_iid_lay)])

    layer_override(os.path.dirname(light_rig_name))
    
    maya_wrapper.update_frame_range()
    
    maya_wrapper.delete_unkown_nodes()
    
    file_saving(mode = "CH_Utility")
    dialogue.message("message", config.PRJCODE, "CHAR Utility file successfully created")
    
    
def ch_Line():
    
    scene_cleanup()
    maya_wrapper.import_scene(config.ch_line)
    
    ch_layers = pm.ls("CH_*", type="renderLayer")
    ch_sets = pm.ls("*_CHAR", et="objectSet")
    lighting_wrapper.add_meshes_to_layers(ch_sets, ch_layers)
    
    interaction_mesh_set = pm.PyNode("interaction_mesh_set")
    lighting_wrapper.add_meshes_to_layers([interaction_mesh_set], [ch_layers])
    
    
    maya_wrapper.update_frame_range()
    
    maya_wrapper.delete_unkown_nodes()
    
    pm.setAttr("defaultRenderGlobals.currentRenderer","mayaSoftware")
    pm.setAttr("defaultRenderQuality.shadingSamples",16)
    pm.setAttr("defaultRenderQuality.maxShadingSamples",32)
    pm.setAttr("defaultRenderQuality.pixelFilterWidthX",3)
    pm.setAttr("defaultRenderQuality.pixelFilterWidthY",3)
    pm.setAttr("defaultRenderQuality.redThreshold",1)
    pm.setAttr("defaultRenderQuality.greenThreshold",1)
    pm.setAttr("defaultRenderQuality.blueThreshold",1)
    pm.setAttr("defaultRenderGlobals.oversamplePaintEffects",1)
    pm.setAttr("defaultRenderGlobals.oversamplePfxPostFilter",1)
    pm.setAttr("defaultRenderGlobals.imageFormat",3)
    
    
    file_saving(mode = "CH_Line")
    dialogue.message("message", config.PRJCODE, "CHAR Line file successfully created")
    

def scene_cleanup():
    pm.editRenderLayerGlobals(crl="defaultRenderLayer")
    pm.delete(pm.ls(["MasterLightGrp", "CHAR_LightRIg", "INT_LIGHTS", "rim_lights", "CH_SHD_LIGHTS"]))
    pm.delete(pm.ls(["BG_*", "CH_*"], type="renderLayer"))
    pm.delete(pm.ls(type="RedshiftAOV"))
    pm.delete(pm.ls(["SHD_CATCHER", "CH_RIM_SHD", "CH_RIM_SHD_FRESNEL", "CH_RIM_SHD_SG"]))

def get_shot_wise_light_rig_name():
    shot_lighting_path = os.path.join(config.get_shot_path(ep, seq, shot), "lighting")
    json_file_name = ep + "_" + seq + "_" + shot + "_" + "shot_Data.json"
    json_path = os.path.join(shot_lighting_path, json_file_name)
    data = utility.read_json_file(json_path)
    light_rig_name = data["light_rig_name"]
    light_rig_path = os.path.join(config.bg_preset_path, light_rig_name, light_rig_name)
    return light_rig_path

def file_saving(mode = None, cts = True):
    maya_wrapper.delete_unkown_nodes()
    shot_details = maya_wrapper.get_scene_details_from_scene_name()
    local_path = os.path.join(config.maya_temp_path, shot_details[3])
    file_path = maya_wrapper.save_scene_as(local_path, shot_details[3], mode)
    pm.mel.eval("redshiftUpdateActiveAovList()")
    if cts:
        copy_to_server(file_path)

def copy_to_server(current_file_path):
    shot_lighting_path = os.path.join(config.get_shot_path(ep, seq, shot), "lighting")
    if not os.path.exists(shot_lighting_path):
        os.makedirs(shot_lighting_path)
    shutil.copy2(current_file_path, shot_lighting_path)

def layer_override(path):
    for each_text in os.listdir(path):
        layer_name = each_text.split(".")[0]
        print "layer_name", layer_name
        if pm.objExists(layer_name):
            pm.editRenderLayerGlobals(crl=layer_name)
            text_path = os.path.join(path, each_text)
            data = utility.read_text_file(text_path)
            for each_line in data:
                eval(each_line)

def save_file_to_server():
    pm.saveFile(f=1)
    scene_full_path = maya_wrapper.get_scene_name(full_path=True)
    copy_to_server(scene_full_path)
    pm.confirmDialog(m = "copied to server", b="Ok")