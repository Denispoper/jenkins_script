import maya.cmds as mc
import sys
import argparse
import maya.mel as mel
import maya.app as ma
import random
import maya.standalone as ms

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    temp = tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
    res = [float(i)/255.0 for i in temp]
    return res

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
    parser.add_argument('-lt', '--lighttype', default='Physical', type=str)
    parser.add_argument('-mc', '--materialcount', default=1, type=int)
    parser.add_argument('-lc', '--lightcount',nargs='?', const=True, default=1, type=int)
    parser.add_argument('-ibl', '--isibl', default=False, type=str2bool)
    parser.add_argument('-ms', '--maxsamples', default=200, type=int)
    parser.add_argument('-th', '--threshold', default=0.005, type=float)

    return parser
    
def createLight(type, index): 
    if(type == 'IES'): 
        light = createIESLight(index)
    elif(type == 'Physical'): 
        light = createPhLight(index)
    else: 
        raise argparse.ArgumentError('Wrong name of type')
    
    if(mc.objExists(light)):
        mc.rotate(-90, 0, 0, light)
        mc.move(0, 3, 0, light)

    return light

def createLights(type, count):
    for index in range(count):
        light = createLight(type, index)
        mc.setAttr('{}.translateZ'.format(light), -3 * (index // 3))
        mc.setAttr('{}.translateX'.format(light), 3 * (index % 3))

def createIBL():
    light = mc.createNode( 'transform', n='RPRIBL' )
    mc.createNode('RPRIBL', n='RPRIBLLight', p='RPRIBL')

    mc.scale(1000, 1000, 1000, light)

    mc.setAttr('RPRIBLLight.intensity', 0.01)

def createPhLight(index):
    light = mc.createNode('transform', n='PhysicalLight{}'.format(index))
    lShape = mc.createNode('RPRPhysicalLight', n='RPRPhLightShape{}'.format(index), p=light)
    mc.setAttr('{}.lightIntensity'.format(lShape), 0.5)

    return light

def createIESLight(index): 
    light = mc.createNode('transform', n='RPRIES{}'.format(index))
    mc.createNode('RPRIES', n='RPRIESLight{}'.format(index), p=light)

    rootPath = 'D:\MayaMaterials'
    filePath = rootPath + '/ies-lights-pack/pear.ies'
    mc.setAttr('RPRIESLight{}.iesFile'.format(index), filePath, type='string')
    mc.scale(0.03, 0.03, 0.03, light)
    
    return light

def changeThreshold(value):
    mc.setAttr('RadeonProRenderGlobals.adaptiveThreshold', value)

def changeMaxSamples(value):
    mc.setAttr('RadeonProRenderGlobals.completionCriteriaIterations', value)

def setCamera(objCount):
    if(mc.objExists('persp')):
        mc.setAttr('persp.translateX', 10)
        mc.setAttr('persp.rotateX', -45)

        mc.setAttr('persp.translateY', 10)
        mc.setAttr('persp.rotateY', 90)

        mc.setAttr('persp.translateZ', -5)
        mc.setAttr('persp.rotateZ', 0)

def setParamerts():
    mc.setAttr('defaultRenderGlobals.imageFormat', 8)

def createObjects(node, objCount, materialCount):
    
    createUberMaterials(materialCount)
    
    for index in range(objCount):
        transNode = mc.createNode('transform', n="p{}{}".format(node, index))
        pShape = mc.createNode('mesh', n='p{}Shape{}'.format(node, index), parent=transNode)
        polyNode = mc.createNode('poly{}'.format(node), n='poly{}{}'.format(node, index))
        mc.connectAttr('{}.output'.format(polyNode), '{}.inMesh'.format(pShape), f=True)
        mc.sets('{}'.format(pShape), e=True, forceElement='initialShadingGroup')
        mc.setAttr('{}.translateZ'.format(transNode), -3 * (index // 3))
        mc.setAttr('{}.translateX'.format(transNode), 3 * (index % 3))
        applyRPRUberMaterial(index % materialCount, pShape)

def createUberMaterials(count):
    for index in range(count):
        shd = mc.shadingNode('RPRUberMaterial', name="RPRUberMaterial{}".format(index), asShader=True)
        shdSG = mc.sets(name='{}SG'.format(shd), empty=True, renderable=True, noSurfaceShader=True)
        mc.connectAttr('{}.outColor'.format(shd), '{}.surfaceShader'.format(shdSG))
        color = "%06x" % random.randint(0, 0xFFFFFF)
        color = hex_to_rgb(color)
        mc.setAttr('{}.diffuseColor'.format(shd), color[0], color[1], color[2], type='double3')

def applyRPRUberMaterial(shadingGroupIndex, polyNode):
    mc.sets(polyNode, e=True, forceElement='RPRUberMaterial{}SG'.format(shadingGroupIndex))


def makeImage():
    mc.setAttr('defaultRenderGlobals.imageFormat', 8)
    

ms.initialize("Python")

mc.loadPlugin("Mayatomr") # Load all plugins you might need
mc.loadPlugin("RadeonProRender")

if __name__ == "__main__":
    parser = createParser()
    ns = parser.parse_args(sys.argv[1:])

    print(ns)

    createObjects(ns.objecttype, ns.objectcount, ns.materialcount)
    createLights(ns.lighttype, ns.lightcount)
    if(ns.isibl):
        createIBL()
    changeMaxSamples(ns.maxsamples)
    changeThreshold(ns.threshold)

    makeImage()

#D:\Autodesk\Maya\Maya2019\bin>mayapy D:\Workspace\test_scpirts\test.py -ot 'Cube'