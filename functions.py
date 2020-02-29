import maya.cmds as mc
import sys
import argparse    

def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-ot', '--objecttype', default='Cube', type=str)
    parser.add_argument('-oc', '--objectcount', default=1, type=int)
    parser.add_argument('-lt', '--lighttype', default='Physical Light', type=str)
    parser.add_argument('-mc', '--materialcount', default=1, type=int)
    parser.add_argument('-lc', '--lightcount',nargs='?', const=True, default=1, type=int)
    parser.add_argument('-ibl', '--isibl', default=False, type=str2bool)
    parser.add_argument('-ms', '--maxsamples', default=200, type=int)
    parser.add_argument('-th', '--threshold', default=0.005, type=float)

    return parser
    
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

def createObjects(node, count):
    for index in range(count):
        parNode = mc.createNode('transform', n="p{}{}".format(node, (index + 1)))
        mc.createNode('mesh', n='p{}Shape{}'.format(node, (index + 1)), parent=parNode)
        mc.createNode('poly{}'.format(node), n='poly{}{}'.format(node, (index + 1)))
        mc.connectAttr('poly{}{}.output'.format(node, (index + 1)), 'p{}Shape{}.inMesh'.format(node, (index + 1)), f=True)
        mc.sets('p{}Shape{}'.format(node, (index + 1)), e=True, forceElement='initialShadingGroup')



    

def createUberMaterials(count):
    print('')

    #D:\Autodesk\Maya\Maya2019\bin>mayapy D:\Workspace\test_scpirts\test.py -ot 'Cube'

def setParamerts():
    mc.setAttr('defaultRenderGlobals.imageFormat', 8)