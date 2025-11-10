#!/usr/bin/env python3

import data_tools
import sim_wrappers
import numpy as np
import robotic as ry

def rai2mujoco(which):
    C = ry.Config()
    if which=='franka':
        C.addFile('$HOME/git/rai-robotModels/panda/panda.g')
        C.getFrame('panda_finger_joint1').setJoint(ry.JT.none)
        C.getFrame('panda_finger_joint2').setJoint(ry.JT.none)
    elif which=='twoFingers':
        # C.addFile('../sim-wrappers/sample/twoFingers.yml')
        C.addFile('../../25-ExploreThroughSim/twoFingersBall.yml')
        C.getFrame('obj').unLink()
    elif which=='oneFinger':
        C.addFile('../../25-ExploreThroughSim/oneFingerBall.yml')
        C.getFrame('obj').unLink()
    else:
        raise Exception()

    M = data_tools.MujocoWriter(C)
    M.dump()
    xml = M.str()
    with open('z.xml', 'w') as fil:
        fil.write(xml.decode('ascii'))
    # exit()

    print(C.getJointNames())

    sim = sim_wrappers.MjSim(xml, C, use_mj_viewer=True)
    while sim.ctrl_time<2.:
        sim.step([], .1, view_speed=1.)
        q = C.getJointState()
        q = q[:sim.ctrl_dim]
        q += .1 * np.random.randn(q.size)
        sim.ctrl.overwriteSmooth(q.reshape(1,-1), [.2], sim.ctrl_time)

if __name__ == "__main__":
    # rai2mujoco('franka')
    # rai2mujoco('twoFingers')
    rai2mujoco('oneFinger')
