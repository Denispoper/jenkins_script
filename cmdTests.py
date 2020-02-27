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


if __name__ == "__main__":
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])

    print(namespace)

    

