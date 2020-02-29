import maya.standalone as ms
import maya.cmds as mc
import functions as f

ms.initialize("Python")

mc.loadPlugin("Mayatomr") # Load all plugins you might need
mc.loadPlugin("RadeonProRender")

if __name__ == "__main__":
    parser = f.createParser()
    namespace = parser.parse_args(f.sys.argv[1:])

    print(namespace)