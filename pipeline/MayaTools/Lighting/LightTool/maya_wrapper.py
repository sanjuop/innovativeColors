import os
import string
import random
import logging
import shutil

import maya.mel as mel
import maya.OpenMayaUI
import maya.cmds as cmds
import pymel.core as pm

from shiboken2 import wrapInstance
import PySide2.QtWidgets as QtWidgets
import PySide2.QtCore as QtCore
import PySide2.QtGui as QtGui

import dialogue as dialogue;reload(dialogue)
import config as config;reload(config)


def update_camera():
    allcams=pm.ls(type="camera")
    for each_cam in allcams:
        pm.setAttr(each_cam+".renderable",0)
    if pm.objExists("cam01:cameraRig_hand_camShape"):
        render_cam = pm.PyNode("cam01:cameraRig_hand_camShape")
        render_cam.nearClipPlane.set(0.1)
        render_cam.renderable.set(1)


def delete_unkown_nodes():
    import pymel.core as pm
    for each_un in pm.ls(type="unknown"):
        if pm.objExists(each_un):
            if each_un.isLocked():
                each_un.unlock()
            pm.delete(each_un)


def update_frame_range():
    startFrame = pm.playbackOptions(q=1,ast=True)
    endFrame = pm.playbackOptions(q=1,aet=True)
    rg_node = pm.PyNode("defaultRenderGlobals")
    rg_node.startFrame.set(startFrame)
    rg_node.endFrame.set(endFrame)

def set_default_render_layer():
    ren_lay = pm.PyNode("defaultRenderLayer")
    ren_lay.attr("renderable").set(0)
    ren_lay.setCurrent()

def load_render_globals():
    prj_code = config.PRJCODE
    preset_path = os.listdir(config.render_global_presets)
    for each_preset in preset_path:
        file_path = os.path.join(config.render_global_presets, each_preset)
        shutil.copy2(file_path, pm.internalVar(ups=True))

    pm.nodePreset(load=("redshiftOptions", "RGP1_%s" % prj_code))
    pm.nodePreset(load=("defaultRenderGlobals", "RGP2_%s" % prj_code))
    pm.nodePreset(load=("defaultResolution", "RGP3_%s" % prj_code))

    pm.mel.eval('unifiedRenderGlobalsWindow;')


def maya_main_window():
    main_window_ptr = maya.OpenMayaUI.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


def new_scene():
    checkState()
    return cmds.file(new=True, f=True)


def rewind():
    cmds.currentTime(1)    
    cmds.playbackOptions(minTime=1)


def get_scene_name(full_path=False, basename=False, dir_base=False):
    scene_name = pm.sceneName()
    if scene_name == "":
        pm.confirmDialog(m="File not open",b="Ok")
        return
    elif full_path:
        abspath = scene_name.abspath()
        return abspath
    elif basename:
        basename = scene_name.basename()
        return basename
    elif dir_base:
        dir_path = scene_name.dirname()
        basename = scene_name.basename()
        return [dir_path,basename]


def get_scene_details_from_scene_name():
    scene_basename = get_scene_name(basename=True)
    if scene_basename is not None:
        shot_name = scene_basename.split("_")[1]
        episode = shot_name.split("-")[0]
        sequence = shot_name.split("-")[1]
        shot = shot_name.split("-")[2]
        return episode, sequence, shot, shot_name


def save_scene_as(path=None, file_name=None, file_mode="master", version="v01_i01", file_type=".ma"):
    delete_unkown_nodes()
    if not os.path.exists(path):
        os.makedirs(path)
    if file_mode == "master":
        file_name = os.path.join(file_name, file_mode, version+file_type).replace("\\", "_")
    else:
        file_name = os.path.join(config.PRJCODE, file_name, file_mode, version + file_type).replace("\\", "_")
    full_path = os.path.join(path, file_name)
    delete_unkown_nodes()
    pm.saveAs(full_path)
    return full_path


def add_custom_attr(node_name, value, attr_name):
    node_name = pm.PyNode(node_name)
    if not node_name.hasAttr(attr_name):
        pm.addAttr(node_name,shortName=attr_name, longName=attr_name, dataType='string')
    pm.setAttr(node_name+".{}".format(attr_name), value, type="string")


def get_meshes_from_top_group(top_group,fp=False):
    print "top_group",top_group
    all_nodes = top_group.nodes()
    # all_meshes = [i for i in all_nodes.listRelatives(ad=1, type=["mesh", "nurbsSurface"])]
    all_meshes = pm.ls(all_nodes, type=["mesh", "nurbsSurface"])
    if fp:
        all_trans_nodes = [eachMesh.getParent().fullPath() for eachMesh in all_meshes]
    else:
        all_trans_nodes = list(set([str(eachMesh.getParent()) for eachMesh in all_meshes]))
    return all_trans_nodes



def add_meshes_to_layer(layer_names, sets):
    meshes = [pm.sets(each, q=1) for each in sets]
    all_meshes = [mesh for each_grp in meshes for mesh in each_grp]
    for each_lay in layer_names:
        pm.editRenderLayerMembers(each_lay, all_meshes)


def userPrefDir():
    return cmds.internalVar(userPrefDir=True)


def open_scene(path = None):
    if os.path.exists(path):
        checkState()
        insert_recent_file(path)
        opend = cmds.file(path, o = True, f = True, esn = True)
        logging.info("{}".format(opend))
        return opend


def insert_recent_file(path):
    cmds.optionVar(stringValueAppend=('RecentFilesList', path))


def current_open_file():
    return cmds.file(q=True,sn=True)              

def checkState():
    # check if there are unsaved changes
    fileCheckState = cmds.file(q=True, modified=True)

    # if there are, save them first ... then we can proceed 
    if fileCheckState:
      # This is maya's native call to save, with dialogs, etc.
      # No need to write your own.
      if dlg.warning("warning", "Scene Not Saved", "Scene Not Saved, Do you want to save it first?"):
        cmds.SaveScene()
      pass
    else:
      pass
      
      
def reference_scene(path = None):
    if os.path.exists(path):
        namesspace = files.file_name_no_extension(files.file_name(path))
        return cmds.file(path, r = True, f = True, ns = namesspace, esn = False)    
        
def import_scene(path=None, namespace=None):
    if os.path.exists(path):
        if namespace:
            pm.importFile(path)
        else:
            pm.importFile(path)

        

def list_references():
    results = {}
    allReferences = pm.listReferences(loaded=True,recursive=True)
    for each_Ref in allReferences:
        results[str(each_Ref.namespace)] = each_Ref
    
    return results
            
     
def relink_pathes(project_path = None):
    results = []
    links = cmds.filePathEditor(query=True, listDirectories="")
    for link in links:
        pairs =  cmds.filePathEditor(query=True, listFiles=link, withAttribute=True, status=True)
        '''
        paris: list of strings ["file_name node status ...", "file_name node status ...",...]
        we need to make this large list of ugly strings (good inforamtion seperated by white space) into a dictionry we can use
        '''        
        l = len(pairs)
        items = l/3 
        order = {}
        index = 0
        
        '''
        order: dict of {node: [file_name, status],...}
        '''
        
        for i in range(0,items):
            order[pairs[index+1]] = [pairs[index],pairs[index+2]]
            index = index + 3  
                        
        for key in order:            
            # for each item in the dict, if the status is 0, repath it
            if order[key][1] == "0": 
                if repath(key,order[key][0],project_path):
                    results.append(key)
                    
                   
    return results

    
    
def repath(node, file, project_path):
    matches = []
    for root, dirnames, filenames in os.walk(project_path):
        for x in filenames:
            if x == file:
                matches.append([root,os.path.join(root, x)]) 
            elif x.split(".")[0] == file.split(".")[0]: #---> this second option is used when a file is useing ##### padding, we can match by name only
                
                x_ext = x.split(".")[len(x.split("."))-1]
                file_ext = file.split(".")[len(file.split("."))-1]
                if x_ext == file_ext:
                    matches.append([root,os.path.join(root, x)])
                
                
    if len(matches)>0:   
        return cmds.filePathEditor(node, repath=matches[0][0])      
     
    return None                           

    
def snapshot(path = None, width = 96, height = 96):
    current_image_format = cmds.getAttr("defaultRenderGlobals.imageFormat")
    cmds.setAttr("defaultRenderGlobals.imageFormat", 32) # *.png
    #path = "/Users/liorbenhorin/Library/Preferences/Autodesk/maya/2015-x64/scripts/pipeline/thumb.png"
    cmds.playblast(cf = path, fmt="image", frame = cmds.currentTime( query=True ), orn=False, wh = [width,height], p=100, v=False)
    cmds.setAttr("defaultRenderGlobals.imageFormat", current_image_format)
    
    if os.path.isfile(path):
        return path
    else:
        return False


def playblast_snapshot(path = None,format = None, compression = None, hud = None, offscreen = None, range=None, scale = None):
    current_image_format = cmds.getAttr("defaultRenderGlobals.imageFormat")
    cmds.setAttr("defaultRenderGlobals.imageFormat", 32) # *.png

    if range is None:
        
        range = playback_selection_range()
        print range
        if range is None:
        
            start = cmds.playbackOptions( q=True,min=True )
            end  = cmds.playbackOptions( q=True,max=True )
            range = [start, end]
     
    cmds.playblast(frame =int((range[0] + range[1])/2), cf = path, fmt="image",  orn=hud, os=offscreen, wh = scene_resolution(), p=scale, v=False) 
    
    cmds.setAttr("defaultRenderGlobals.imageFormat", current_image_format)


def playblast(path = None,format = None, compression = None, hud = None, offscreen = None, range=None, scale = None):
    if range is None:
        
        range = playback_selection_range()
        print range
        if range is None:
        
            start = cmds.playbackOptions( q=True,min=True )
            end  = cmds.playbackOptions( q=True,max=True )
            range = [start, end]
     
    cmds.playblast(startTime =range[0] ,endTime =range[1], f = path, fmt=format,  orn=hud, os=offscreen, wh = scene_resolution(), p=scale, qlt=90,c=compression, v=True, s = qeury_active_sound_node())


def qeury_active_sound_node():
    aPlayBackSliderPython = mel.eval('$tmpVar=$gPlayBackSlider')
    sound = cmds.timeControl(aPlayBackSliderPython, q=1, s=1)
    if sound:
        return sound
    else:
        return None

def playback_selection_range():
    aPlayBackSliderPython = mel.eval('$tmpVar=$gPlayBackSlider')
    time_selection = cmds.timeControl( aPlayBackSliderPython, q=True,rng=True )[1:-1]
    start = round(float(time_selection.split(":")[0]))
    end = round(float(time_selection.split(":")[1]))
    
    if start+1 == end:
        return None
    else:
        return [start, end]    

def getPlayblastOptions():
    options = {}
    options["format"] = cmds.playblast(q=True,fmt=True)
    options["compression"] = cmds.playblast(q=True,c=True)
    return options
    
def maya_api_version():
    return int(cmds.about(api=True))

def scene_resolution():
    return [cmds.getAttr("defaultResolution.width"),cmds.getAttr("defaultResolution.height")]
    

def create_scriptjob(parent = None, event = None, script = None):
    if event and script:

        return cmds.scriptJob(e=[event,script], ro=False, p = parent)
        
def kill_scriptjob(job = None):
    if job:

        return cmds.scriptJob(kill = job, f = True)       

def new_scene_script(parent = None, script = None):
    return create_scriptjob(parent = parent, event = "NewSceneOpened", script = script)   

def open_scene_script(parent = None, script = None):
    return create_scriptjob(parent = parent, event = "SceneOpened", script = script)   

def new_scene_from_selection(project_path = None, mode = "include"):
    temp_file = os.path.join(project_path, "scenes", "temp_%s.ma"%(id_generator()))
    logging.info(temp_file)
    sel = cmds.ls(sl=True)
    if len(sel)>0:
        if mode == "include":
            saved_file = cmds.file(temp_file, type='mayaAscii', exportSelected=True, expressions=True, constraints=True, channels=True, constructionHistory=True, shader=True)    
        if mode == "exclude":
            saved_file = cmds.file(temp_file, type='mayaAscii', exportSelected=True, expressions=False, constraints=False, channels=False, constructionHistory=False, shader=True)
        
        if saved_file:
            open_scene(saved_file)
            return saved_file
    
    return None


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def maya_version():
    return cmds.about(version=True)
    

def set_fps(fps = None):
    fps_string = "pal"
    if fps == 25:
        fps_string = "pal"
    if fps == 24:
        fps_string = "film"
    if fps == 30:
        fps_string = "ntsc"                
    cmds.currentUnit(t=fps_string)


def clean_up_file():
    pass
    # import references
    """
    refs = cmds.ls(type='reference')
    for i in refs:
        rFile = cmds.referenceQuery(i, f=True)
        cmds.file(rFile, importReference=True, mnr=True)    
        
    defaults = ['UI', 'shared']

    # Used as a sort key, this will sort namespaces by how many children they have.
    def num_children(ns):
        return ns.count(':')

    namespaces = [ns for ns in cmds.namespaceInfo(lon=True, r=True) if ns not in defaults]
    # We want to reverse the list, so that namespaces with more children are at the front of the list.
    namespaces.sort(key=num_children, reverse=True)

    for ns in namespaces:

        if namespaces.index(ns)+1 < len(namespaces):
            parent_ns = namespaces[namespaces.index(ns)+1]   
            cmds.namespace(mv=[ns,parent_ns], f=True) 
            cmds.namespace(rm=ns) 
        else:
            cmds.namespace(mv=[ns,":"], f=True)  
            cmds.namespace(rm=ns) 
    
    # remove ngSkinTools custom nodes
    from ngSkinTools.layerUtils import LayerUtils 
    LayerUtils.deleteCustomNodes()
    
    # remove RRM proxies
    if cmds.objExists("RRM_MAIN"):
        cmds.select("RRM_MAIN",hi=True)
        proxies = cmds.ls(sl=True)
        cmds.lockNode(proxies,lock=False)
        cmds.delete(proxies)
        
        if cmds.objExists("RRM_ProxiesLayer"):
            cmds.delete("RRM_ProxiesLayer")"""
            
def viewMassage(text = None):
            cmds.inViewMessage( amg="Pipeline: " + text, pos='topCenter', fade=True, fst = 3000 )
        