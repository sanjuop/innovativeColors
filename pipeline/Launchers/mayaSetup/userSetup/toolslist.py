import os
import sys

PIPELINE_PATH = os.environ.get("PIPELINE_PATH").split("pipeline")[0]
if PIPELINE_PATH not in sys.path:
    sys.path.append(PIPELINE_PATH)


def asset_manager(*args):
    import pipeline.MayaTools.AssetManager.AssetPublishTool as AMT;reload(AMT)
    AMT.main()

def UVSnapshotExporter(*args):
    import pipeline.MayaTools.Texturing.UVSnapshotExporter.uvSnapshotExporter as UVSE ;reload(UVSE)
    UVSE.Exporter()

def samePolyCount(*args):
    import pipeline.MayaTools.Modeling.SamePolyCount.SamePolyCount as SPC;reload(SPC)
    SPC.samepoly()

def CheckerSizeTool(*args):
    import pipeline.MayaTools.Modeling.CheckerSizeTool.CheckerSizeTool as CST;reload(CST)
    CST.show_window()

def shaderRenamer(*args):
    import pipeline.MayaTools.Shading.shaderRenamer.shaderRenamer as SR;reload(SR)
    SR.main()
    
def LightTool(*args):
    import pipeline.MayaTools.Lighting.LightTool.lighting as LT;reload(LT)
    LT.main() 

def shaderLibrary(*args):
    print "sdfsdfsdfsd"
