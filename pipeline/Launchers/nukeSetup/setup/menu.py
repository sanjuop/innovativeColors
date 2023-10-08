import os
import nuke

import config
import loadSettings
import knobsettings
import tools

def nuke_startup_settings():
    """
    Process of getting project info from project database (DB: Projects) and setting while opening nuke 
    return: None

    """
    nuke.addOnCreate(lambda: loadSettings.NukeSettings.set_lut_setting(monitorLut=config.nuke_data["monitor"], 
                                                                       intLut8=config.nuke_data["intLut8"],
                                                                       intLut16=config.nuke_data["intLut16"],
                                                                       logLut=config.nuke_data["log"],
                                                                       floatLut=config.nuke_data["floatLut"]),
                                                                        nodeClass='Root')
                                                                       
                                                                        

    nuke.addOnCreate(lambda: loadSettings.NukeSettings.set_project_setting(screen_width=config.width,
                                                                            screen_height=config.height, 
                                                                            project=config.code,
                                                                            frame_rate=config.fps), 
                                                                            nodeClass='Root')

    # nuke.addOnCreate(lambda: loadSettings.NukeSettings.set_viewer_setting(viewerProcessValue=config.nuke_data["viewer"]),
    #                                                                         nodeClass='Viewer')



def call_backs_for_nodes():
    """
    Process of setting call back nodes
    return: None
    """
    root = nuke.root().name()
    nuke.knobDefault('%s.onScriptLoad' % root,
                     'settings.NukeSettings.on_load_setting ()')

    nuke.knobDefault('%s.onScriptSave' % root,
                     'settings.NukeSettings.on_save_setting ()')


def knob_defaults():
    """
    Process of setting knob defaults settings 
    return: None
    """
    knobsettings.knob_default(env_str=config.env_path)


def load_gizmos():
    """
    Process of loading common and project based gizmos in nuke 
    return: None
    """
    common_gizmo_path = os.path.join (config.setup_path, 'gizmos', 'common') 
    gizmo_creation(common_gizmo_path, 'common')
    project_gizmo_path = os.path.join(config.setup_path, 'gizmos', config.code) 
    gizmo_creation(project_gizmo_path, config.code)

def gizmo_creation(gizmo_path, type):
    """
    Process of getting creation of gismos :
    param gizmo path: Gizmos Path
    param type: Type of Gizmos
    return: None
    """
    if os.path.exists(gizmo_path):
        nuke.pluginAddPath(gizmo_path) 
        toolbar=nuke.menu ('Nodes')
        icon = 'icon03.png' if type == 'common' else 'gear_tools.png'

        myMenu = toolbar.addMenu (type, icon-icon)
        for each_gizmo in os.listdir (gizmo_path):
            each_gizmo = each_gizmo.split(".") [0]
            myMenu.addCommand(each_gizmo, 'nuke.createNode ("[giz}")'.format (giz=each_gizmo))

def load_tools():
    """
    Process of loading Production Nke Tools
    return: None
    """
    tools.load_tools (config.code)


nuke_startup_settings()
# call_backs_for_nodes()
# knob_defaults()
# load_gizmos()
# load_tools()