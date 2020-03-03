import maya.standalone as ms
import maya.cmds as mc
import functions as f

ms.initialize("Python")

mc.loadPlugin("Mayatomr") # Load all plugins you might need
mc.loadPlugin("RadeonProRender")

if __name__ == "__main__":
    parser = f.createParser()
    ns = parser.parse_args(f.sys.argv[1:])

    print(ns)

    f.createObjects(ns.objecttype, ns.objectcount, ns.materialcount)
    f.createLights(ns.lighttype, ns.lightcount)
    if(ns.isibl):
        f.createIBL()
    f.changeMaxSamples(ns.maxsamples)
    f.changeThreshold(ns.threshold)
    f.createMetadata(ns)
    f.makeImage()
    f.setCamera(ns.objectcount)


#>mayapy D:\Workspace\test_scpirts\test.py -ot 'Cube' ... 

#>render -r FireRender -proj mayaimages -rd C:\Users\Denispoper\Desktop\mayaimages -of jpeg -im test1 -x 1000 -y 1000 C:\Users\Denispoper\Desktop\mayaimages\test.mb