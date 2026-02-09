#!/usr/bin/env python3

import mesh_tools as mt
from pathlib import PurePath, Path
import os
import glob

path = '../data-tools/sample/shapenet/'

files = sorted(glob.glob(path+'original-obj/*.obj'))

for file in files:
    
    ### load
    mesh = mt.MeshTool(file)
    if mesh==None:
        continue

    mesh.texture2vertexColors()

    ### scale
    mesh.autoScale()
    print('scale:', mesh.tmesh.scale, 'centroid:', mesh.tmesh.centroid)

    ### meshlab repair
    mesh.report()
    mesh.repair_meshlab()
    mesh.report()

    ### trimesh repair
    mesh.repair_trimesh()
    print('  watertight:', mesh.tmesh.is_watertight)
    print('  oriented:', mesh.tmesh.is_winding_consistent)
    # if not mesh.tmesh.is_watertight or mesh.tmesh.is_empty:
        # print('  -- skipping')
        # continue



    ### export .ply
    filebase = os.path.splitext(file)[0]
    name = PurePath(filebase).name
    Path(path+'processed/').mkdir(parents=True, exist_ok=True)
    mesh.export_ply(path+'processed/'+name+'.ply')

    mesh.createDecomposition()

    ### export .mesh.h5
    mesh.export_h5(path+'processed/'+name+'.h5', without_colors=True, inertia=True)

    print('=== done: ', file)


