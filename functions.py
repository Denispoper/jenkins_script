import maya.cmds as mc

def createLight(type): 
    if(type == 'IES'): 
        light = createIESLight()
    elif(type == 'Physical'): 
        light = createPhLight()
    else: 
        print('error')
    
    if(mc.objExists(light)):
        mc.move(0, 10, 0, light)
        mc.rotate(-90, 0, 0, light)


def createIBL():
    light = mc.createNode( 'transform', n='RPRIBL' )
    mc.createNode('RPRIBL', n='RPRIBLLight', p='RPRIBL')

    mc.scale(1000, 1000, 1000, light)

    mc.setAttr('RPRIBLLight.intensity', 0.003)


def createPhLight():
    light = mc.createNode('transform', n='PhysicalLight')
    mc.createNode('RPRPhysicalLight', n='RPRPhLightShape', p='PhysicalLight')

    return light


def createIESLight(): 
    light = mc.createNode( 'transform', n='RPRIES' )
    mc.createNode('RPRIES', n='RPRIESLight', p='RPRIES')

    rootPath = 'D:\MayaMaterials'
    filePath = rootPath + '/ies-lights-pack/star.ies'
    mc.setAttr('RPRIESLight.iesFile', filePath, type='string')
    
    return light


def changeThreshold(value):
    mc.setAttr('RadeonProRenderGlobals.adaptiveThreshold', value)


def changeMaxSamples(value):
    mc.setAttr('RadeonProRenderGlobals.completionCriteriaIterations', value)

def setCamera(objCount):
    if(mc.objExists('persp')):
        mc.setAttr('persp.translateX', objCount + 0.5)
        mc.setAttr('persp.rotateX', -45)

        mc.setAttr('persp.translateY', objCount + 0.5)
        mc.setAttr('persp.rotateY', 90)

        mc.setAttr('persp.translateZ', 0)
        mc.setAttr('persp.rotateZ', 0)

