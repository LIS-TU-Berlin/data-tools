import subprocess
import os
import yaml
from pathlib import PurePath

class DataInstaller:
    data_home = '$USER@hal-9000.lis.tu-berlin.de:/home/data/'

    def __init__(self, manifest_file, dest_path = './'):
        self.data_home = os.path.expandvars(self.data_home)
        self.data_dest = dest_path
        self.rsync = 'rsync -vrlptzP --update --mkpath'.split()

        # load the manifest
        self.data_src = str(PurePath(manifest_file).parent)+'/'
        manifest_name = str(PurePath(manifest_file).name)
        print('--- base path:', self.data_src)
        cmd = self.rsync + [self.data_home+manifest_file, self.data_dest]
        print('--- loading manifest:', cmd)
        subprocess.run(cmd)

        with open(manifest_name, 'r', encoding='utf-8') as fil:
            self.manifest = yaml.safe_load(fil)

        # print('--- manifest:\n', self.manifest)

    def pull_all(self):
        cmd = self.rsync + [self.data_home+self.data_src, self.data_dest] #'--dry-run', 
        print('--- loading full folder:', cmd)
        subprocess.run(cmd)

    def push_all(self):
        cmd = self.rsync + [self.data_dest, self.data_home+self.data_src, '--dry-run']
        print('--- pushing full folder:', cmd)
        # subprocess.run(cmd)

    def install(self, start=0, stop=-1):
        datasets = self.manifest['datasets']

        # write files to be copied into file
        with open('z.files', 'w', encoding='utf-8') as fil:
            for d in datasets[start:stop]:
                fil.write(str(PurePath(d).parent)+'/\n')
                fil.write(d+'\n')
            fil.write('- *\n')

        # load them
        cmd = self.rsync + ['--include-from=z.files', self.data_home+self.data_src, self.data_dest]
        print('--- loading datasets:', cmd)
        subprocess.run(cmd)
