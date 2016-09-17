#!/usr/bin/env python3

import math
import numpy
import os
import random
import sys

from moviepy.editor import VideoClip
from vapory import *

def rand_spherical():
    r = pow(random.random(), 1.0/3.0)

    phi = random.uniform(0,2*math.pi)
    costheta = random.uniform(-1,1)
    sintheta = math.sqrt(1-costheta*costheta)
    sinphi = math.sin(phi)
    cosphi = math.cos(phi)

    x = r*sintheta*cosphi
    y = r*sintheta*sinphi
    z = r*costheta

    return numpy.array([x,y,z])

class RungeKutta:
    def __init__(self, initial, derivative=None,
                 dt=1.0):
        self.frames = [initial]
        self.dt = float(dt)

        if derivative is not None:
            self.derivative = derivative
        else:
            self.derivative = lambda t,x : x.derivative(t)


    def __call__(self, t):
        self._advance_beyond(t)
        return self._interpolate_to(t)

    def _advance_beyond(self, t):
        frames_needed = t/self.dt + 2
        while len(self.frames) < frames_needed:
            self._single_step()

    def _single_step(self):
        dt = self.dt
        t = len(self.frames) * self.dt
        yn = self.frames[-1]

        k1 = self.derivative(t, yn)
        k2 = self.derivative(t + dt/2, yn + k1*(dt/2))
        k3 = self.derivative(t + dt/2, yn + k2*(dt/2))
        k4 = self.derivative(t + dt, yn + k2*dt)

        yn_plus1 = yn + (k1 + k2*2 + k3*2 + k4)*(dt/6.0)

        self.frames.append(yn_plus1)

    def _interpolate_to(self, t):
        i_before = int(t/self.dt)
        t_diff = (t/self.dt) % 1.0
        before = self.frames[i_before]
        after = self.frames[i_before + 1]
        return before*(1-t_diff) + after*t_diff

color_index = 0
class PhysicsSphere:
    def __init__(self, pos, vel, color=None):
        self.pos = numpy.array(pos, dtype='float64')
        self.vel = numpy.array(vel, dtype='float64')
        if color is None:
            global color_index
            self.color = ['r','b'][color_index%2]
            color_index += 1
        else:
            self.color = color

    def __add__(self, other):
        return PhysicsSphere(self.pos + other.pos,
                             self.vel + other.vel,
                             self.color)

    def __mul__(self, val):
        return PhysicsSphere(self.pos*val,
                             self.vel*val,
                             self.color)

    def force(self, other):
        disp = other.pos - self.pos
        mag = numpy.linalg.norm(disp)
        disp /= mag

        #force = 1.0/(mag*mag + 1.0)
        r = 1.0
        d = 0.3
        force = 1.0/(1.0 + math.exp((mag-r)/d))
        return force*disp


class SphereMovement:
    def __init__(self, spheres=None):
        if spheres is None:
            self.spheres = []
        else:
            self.spheres = spheres

    def __add__(self, other):
        output = self.__class__()
        for s1,s2 in zip(self, other):
            output.spheres.append(s1+s2)
        return output

    def __mul__(self, val):
        output = self.__class__()
        for s in self:
            output.spheres.append(s*val)
        return output

    def __iter__(self):
        return iter(self.spheres)

    def derivative(self, t):
        output = SphereMovement()
        for s in self:
            # Central potential
            force = -s.pos

            # Damping
            speed = numpy.linalg.norm(s.vel)
            if speed > 0:
                vhat = s.vel/speed
                force -= 0.8*pow(speed,2)*vhat

            # Repulsive
            for other in self:
                if other is not s:
                    force += 2*other.force(s)
            der = PhysicsSphere(s.vel, force)
            output.spheres.append(der)
        return output



initial_spheres = [PhysicsSphere(5*rand_spherical(),[0,0,0])
                   for i in range(20)
                   ]
# initial_spheres = [PhysicsSphere([-3,0,0],[0,0,0]),
#                    PhysicsSphere([3,0,0],[0,0,0]),
#                    ]
rk = RungeKutta(SphereMovement(initial_spheres),
                dt=0.01)

# colors = {'r':Texture(Pigment('color',[1,0,0])),
#           'b':Texture(Pigment('color',[0,0,1])),
#           }
colors = {'r':Texture(Pigment('granite',
                              'scale',2,
                              PigmentMap([0,'rgb',[1,0,0]],
                                         [1,'rgb',[1.0,.4,.4]])
                          )
                  ),
          'b':Texture(Pigment('granite',
                              'scale',2,
                              PigmentMap([0,'rgb',[0,0,1]],
                                         [1,'rgb',[0.4,0.4,1]])
                          )
                  ),
          }

def scene(t):
    camera = Camera(
        'location', [0,-3,5],
        'look_at', [0,0,0],
        'right', '(image_width/image_height)*x',
        'up', 'z',
        'sky', 'z',
        )

    light = LightSource([10,-10,10],
                        'color',1)
    background = Plane('z',-5,
                       Texture(Pigment('color',[0.6,.3,.3])))

    physics_spheres = rk(t)
    spheres = [Sphere(s.pos, 1.0, colors[s.color])
               for s in physics_spheres
           ]
    blob = Blob('threshold', 0.7,
                *spheres)
    return Scene(camera, objects=[light, background]+spheres)


    # spheres = [Sphere(s.pos, 1.5, 1.0, colors[s.color])
    #            for s in physics_spheres
    #        ]
    # blob = Blob('threshold', 0.7,
    #             *spheres)
    # return Scene(camera, objects=[light, background, blob])

def make_frame(t):
    return scene(t).render(width=300, height=200)


final_time = 10

# output_pov = sys.argv[0].replace('.py','.pov')
# with open(output_pov,'w') as f:
#     f.write(str(scene(0)))

output_gif = sys.argv[0].replace('.py','.gif')
VideoClip(make_frame, duration=final_time).write_gif(output_gif, fps=20, program='ffmpeg')

output_png = sys.argv[0].replace('.py','.png')
scene(final_time).render(output_png, width=1200, height=900)
#scene(0).render(output_png, width=1200, height=900)
