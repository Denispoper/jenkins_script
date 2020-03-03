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


#>mayapy D:\Workspace\test_scpirts\test.py -ot Cube -oc 3 -lt Physical -mc 2 -lc 4 -ibl true -ms 400 -th 0.001

#>render -r FireRender -rd C:\Users\Denispoper\Desktop\testResults -of jpeg -im testResultImage -x 1000 -y 1000 C:\Users\Denispoper\Desktop\mayaimages\test.mb