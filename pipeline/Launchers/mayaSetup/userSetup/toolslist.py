import os
import sys

PIPELINE_PATH = os.environ.get("PIPELINE_PATH").split("pipeline")[0]
if PIPELINE_PATH not in sys.path:
    sys.path.append(PIPELINE_PATH)


def asset_manager(*args):
    import pipeline.MayaTools.AssetManager.AssetPublishTool as AMT;reload(AMT)
    AMT.main()


def shaderLibrary(*args):
    print "sdfsdfsdfsd"
