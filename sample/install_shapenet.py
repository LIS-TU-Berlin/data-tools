#!/usr/bin/env python3

import data_tools

if __name__ == "__main__":
    D = data_tools.DataInstaller('shapenet/original-obj.yml')
    D.install(start=0, stop=3)
