#!/usr/bin/env python3

import os

from moviepy.editor import VideoClip
from vapory import *

def scene(t):
    camera = Camera(
        'location', [0,-2,2],
        'look_at', [0,0,0],
        'right', '1.33*x',
        'up', 'z',
        'sky', 'z',
        )

    light = LightSource([10,-10,10],
                        'color',1)


    teardrop = Union(Intersection(Cylinder([0,0,0], [0,0,0.2],
                                           1.0),
                                  Cylinder([0,0.5,-1], [0,0.5,1],
                                           0.5, 'inverse'),
                                  Plane('-x',0),
                              ),
                     Cylinder([0,-0.5,0], [0,-0.5,0.2],
                              0.5))

    rotation = -360*t/2.0
    placement = Object(teardrop,
                       'rotate',[0,0,rotation],
                       'rotate','z*45',
                       Texture(Pigment('color',[1,1,1])))
    placement2 = Object(teardrop,
                        'rotate','z*180',
                        'rotate','y*90',
                        'rotate',[rotation,0,0],
                       'rotate','z*45',
                        Texture(Pigment('color',0.2)))

    background = Box(-50, 50,
                     'inverse',
                     Texture(Pigment('color',[0.6,.3,.3])))

    return Scene(camera, objects=[light, placement, placement2, background])

def make_frame(t):
    return scene(t).render(width=300, height=200)

import ptpython.repl; ptpython.repl.embed(globals(), locals())

# output_png = os.path.join(os.environ['HOME'],
#                           'Downloads','temp.png')
# scene(0).render(output_png, width=400, height=300)

# output_gif = os.path.join(os.environ['HOME'],
#                           'Downloads','temp.gif')
# VideoClip(make_frame, duration=4).write_gif(output_gif, fps=20)
