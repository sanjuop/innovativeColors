import os
import json
import inspect

current_directory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
replace_from = "/anf"
replace_to = "/rdf"
int_set = "interaction_mesh_set"

DRIVE_LETTER = "Q:\\"
# PRJCODE = os.getenv("PRJCODE")
PRJCODE = "lny"
PRJPATH = os.path.join(DRIVE_LETTER, "projects", PRJCODE)
lighting_path = os.path.join(PRJPATH, "Library", "Lighting")
render_global_presets = os.path.join(lighting_path, "renderGlobalPresets")
lighting_preset_path = os.path.join(lighting_path, "LIGHT_PRESET")
bg_preset_path = os.path.join(lighting_preset_path, "BG_LIGHT_RIG")
maya_temp_path = os.path.join(os.path.dirname(os.path.expanduser("~")), "Maya_Temp")
if not os.path.exists(maya_temp_path):
    os.makedirs(maya_temp_path)
matte_id_path = os.path.join(lighting_path, "MATTE_IDs")
bg_utility = os.path.join(lighting_preset_path, "BG_UTILITY.mb")
ch_bty_light_layer_setup = os.path.join(lighting_preset_path, "CH_LIGHT_LAYER_SETUP.mb")
ch_utility = os.path.join(lighting_preset_path, "CH_UTILITY.mb")
ch_line = os.path.join(lighting_preset_path, "CH_LINE.mb")

face_mesh_pattern = r"FaceGeos|FaceGeos_grp"

def get_shot_path(ep, seq, shot):
    lighting_shot_path = os.path.join(PRJPATH, "shots", ep, ep+"-"+seq, ep+"-"+seq+"-"+shot)
    return lighting_shot_path


'''
pm.editRenderLayerGlobals(crl="defaultRenderLayer")
pm.delete(pm.ls(type="RedshiftObjectId"))
pm.delete(pm.ls(type="RedshiftVisibility"))
pm.delete(pm.ls(["*_CHAR*","*_BG*"],type="objectSet"))
pm.delete(pm.ls("MasterLightRig"))
pm.delete(pm.ls(["BG_*","CH_*"], type="renderLayer"))
for e in pm.ls("*:*.OID"):
    e.set(0,type="string")
'''