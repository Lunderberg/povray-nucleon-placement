#!/usr/bin/env python3

from moviepy.editor import VideoClip
import numpy

def make_frame(t):
    frame = numpy.empty(shape=(300,200,3),dtype='int')
    frame.fill(int(t*64))
    return frame

clip = VideoClip(make_frame, duration=4)
clip.write_gif('output_imageio.gif', program='imageio', fps=10)
clip.write_gif('output_imagemagick.gif', program='ImageMagick',
               opt='OptimizePlus',fps=10)
clip.write_gif('output_ffmpeg.gif', program='ffmpeg',fps=10)
