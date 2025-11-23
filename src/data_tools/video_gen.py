import numpy as np
from PIL import Image
from subprocess import Popen, PIPE

class VideoGenerator():
    def __init__(self, framerate=50, filename='tmp.mp4'):
        self.p = Popen(['ffmpeg', '-y', '-loglevel', 'warning', '-f', 'image2pipe',
                        '-vcodec', 'png', '-r', str(framerate), '-i', '-', #input
                        '-vcodec', 'libx264', '-r', '50', '-pix_fmt', 'yuv420p', filename], #output
                       stdin=PIPE)

    def __del__(self):
        self.p.stdin.close()
        self.p.wait()

    def add(self, rgb: np.array):
        Image.fromarray(rgb, 'RGB').save(self.p.stdin, 'PNG')
        