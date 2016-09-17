// Width=400
// Height=300
// FPS=20
// Initial_Clock=0
// Final_Clock=4

#version 3.7;

global_settings {
  assumed_gamma 1
  ambient_light 0
  photons {
    count 100000
  }
}


camera {
  location <0,-5,15>
  look_at <0,0,0>
  right (image_width/image_height)*x
  up z
  sky z
}

light_source {
  <10,-10,10>
  color 1
}

#macro hoop_with_balls(hoop_radius, hoop_thickness, ball_radius, n_balls)
  merge {
    torus{
      hoop_radius hoop_thickness
      rotate 90*x
    }

    #for(i, 1, n_balls)
      sphere{
        <hoop_radius,0,0>, ball_radius
        rotate (360*i/n_balls) * z
      }
    #end
  }
#end


#declare rotation = 360*clock/4;
#declare n_balls = 8;

object {
  hoop_with_balls(4, 0.1, 0.5, n_balls)

  texture {
    pigment{
      rgb 1
    }
  }

  rotate z*(2*rotation)
  translate 4*x
  rotate -z*rotation
}

#for(i, 1, n_balls)
  cylinder {
    <-8,0,-0.5>, <8,0,-0.5>, 0.1
    rotate z*(180*i/n_balls)

    texture{
      pigment{
        rgb <0,1,0>
      }
    }
  }
#end

#declare boundary =
  difference {
    cylinder{<0,0,-1>, <0,0,1>, 8.5}
    cylinder{<0,0,-1.5>, <0,0,1.5>, 8}
  }


object{
  boundary

  texture {
    pigment{
      rgb <1,0,0>
    }
  }
}

// plane{
//   z, -5

//   pigment{
//     rgb 1
//   }
// }
