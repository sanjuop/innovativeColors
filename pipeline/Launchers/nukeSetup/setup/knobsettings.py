import nuke

def knob_default(env_str="Project_Path"):

    nuke.knobDefault("Shuffle.label", "[value in]")
    nuke.knobDefault("ShuffleCopy.label", "[value in] - [value out]")
    nuke.knobDefault("Exposure.mode", "Stops")
    nuke.knobDefault("Roto.output", "rgba")
    nuke.knobDefault("RotoPaint.output", "rgba")
    nuke.knobDefault("Grade.channels", "rgba")
    nuke.knobDefault("PostageStamp.hide_input", "1")
    pref_node = nuke.toNode("preferences")
    pref_node["autoLocalCachePath"].setValue(env_str)