import os
import sys
import config
import nuke

class NukeSettings():
    def __init__(self):
        pass

    @staticmethod
    def set_viewer_settings(viewerProcessValue="sRGB"):
        inst_node = nuke.thisNode()
        inst_node['viewerProcess'].setValue(viewerProcessValue)


    @staticmethod
    def set_lut_setting(monitorLut="sRGB", intLut8="sRGB", intLut16="sRGB", logLut="sRGB", floatLut="sRGB"):
        root = nuke.root()
        root["monitorLut"].setValue(monitorLut)
        root["int8Lut"].setValue(intLut8)
        root["int16Lut"].setValue(intLut16)
        root["logLut"].setValue(logLut)
        root["floatLut"].setValue(floatLut)

    @staticmethod
    def set_project_setting(screen_width=1920, screen_height=1080, project="new_project", frame_rate=24):
        root = nuke.root()
        nuke.addFormat("{} {] {}".format(screen_width, screen_height, project))
        root["format"].setValue(project)
        root["fps"].setValue(frame_rate)
    
    @staticmethod
    def on_load_setting():
        nuke.root()['setLr'].execute()
        nuke.root()['views_colors'].setValue(True)
        if config.stereo == 0:
            try:
                nuke.root().deleteview('left')
                nuke.root().deleteview('right')
                nuke.root().deleteview('main')
            except:
                pass
    
    @staticmethod
    def on_save_settings():
        file_name = nuke.root().name()
        fil_base_name = os.path.basename(file_name).split(".nk")[0]

    @staticmethod
    def on_exit_settings():
        pass
    
    @staticmethod
    def on_create_node(type):
        pass

    @staticmethod
    def set_stereo_settings():
        try:
            nuke.root().addView("main")
        except:
            pass

        try:
            nuke.root().deleteview("left")
        except:
            pass

        try:
            nuke.root().deleteview("right")
        except:
            pass

        