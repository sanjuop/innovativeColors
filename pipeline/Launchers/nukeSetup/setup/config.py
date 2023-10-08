import os
import sys

curr_directory = os.getenv('NUKE_PATH').split('pipeline')[0] 
sys.path.append(curr_directory)

nuke_data = {
    "intLut8": 1.0,
    "intLut16": 1.0,
    "log": 3.0,
    "floatLut": 0.0,
    "viewer": 1.0,
    "monitor": 1.0
}  


width = 1920
height = 1080
fps = 24.0
stereo = "main"
code="GRISU"