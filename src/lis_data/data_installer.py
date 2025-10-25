import subprocess
import os
import yaml
from pathlib import PurePath

class DataInstaller:
    data_src = '$USER@hal-9000.lis.tu-berlin.de:/home/data/'
    data_dest = './'

    def __init__(self, manifest_file):
        self.data_src = os.path.expandvars(self.data_src)
        self.rsync = 'rsync -vrlptzP --update --mkpath'.split()

        # load the manifest
        self.path = str(PurePath(manifest_file).parent)+'/'
        print('== base path:', self.path)
        cmd = self.rsync + [self.data_src+manifest_file, self.data_dest+self.path]
        print('== loading manifest:', cmd)
        subprocess.run(cmd)

        with open(self.data_dest+manifest_file, 'r', encoding='utf-8') as fil:
            self.manifest = yaml.safe_load(fil)
    
    def install(self, start=0, stop=-1):
        datasets = self.manifest['datasets']

        # write files to be copied into file
        with open('z.files', 'w', encoding='utf-8') as fil:
            for d in datasets[start:stop]:
                fil.write(str(PurePath(d).parent)+'/\n')
                fil.write(d+'\n')
            fil.write('- *\n')

        # load them
        cmd = self.rsync + ['--include-from=z.files', self.data_src+self.path, self.data_dest+self.path]
        print('== loading data files:', cmd)
        subprocess.run(cmd)
