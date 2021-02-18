import maya.cmds as cmds
def samepoly():
    #
    sel =cmds.ls(selection=True)
    count=cmds.polyEvaluate( sel,v=True, f=True )
    #print count['vertex','face']
    allgeos =cmds.ls(geometry=True)
    samecount=[]
    for obj in allgeos:
        #
        objcount=cmds.polyEvaluate( obj,v=True, f=True )
        if objcount == count:
            #
            samecount.append(obj)
        else:
            pass
                
    cmds.select(samecount)
    cmds.pickWalk(d='up')
