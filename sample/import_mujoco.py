from data_tools.mujoco_io import MujocoLoader
from data_tools.yaml_helper import dict_as_yaml
import mujoco

def main():
    M = MujocoLoader('../../../tmp/right_hand.xml', verbose=10)
    C = M.C

    with open('allegro_raw.yml', 'w') as fil:
        fil.write(dict_as_yaml(C.asDict()))

    print('org #frames: ', C.getFrameDimension())
    C.view(True)

    C.processStructure(False, True, False, False)
    C.processInertias(recomputeInertias=True)
    C.processStructure(False, True, False, False)
    print('simplified #frames: ', C.getFrameDimension())
    # if processMeshes:
    #     C.writeMeshes(f'{name}_meshes/', copyTextures=True, enumerateAssets=True)
    #     for file in sorted(glob.glob(f'{name}_meshes/*.h5')):
    #         M = ry.MeshHelper(file)
    #         if M.mesh is None:
    #             continue
    #         M.repair(mergeTolerance=1e-4)
    #         M.export_h5()
    C.view(True)

    with open('allegro.yml', 'w') as fil:
        fil.write(dict_as_yaml(C.asDict()))

main()