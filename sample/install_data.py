import lis_data as ld

if __name__ == "__main__":
    D = ld.DataInstaller('shapenet/original-obj.yml')
    D.install(start=0, stop=3)
