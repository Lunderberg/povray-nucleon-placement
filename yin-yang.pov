// Width=1200
// Height=900
// FPS=10
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
  location <-0.5,-2,2>
  look_at <-0.5,0,0>
  right (image_width/image_height)*x
  up z
  sky z
}

light_source {
  <10,-10,10>
  color 1
}

#declare teardrop_thickness = 0.02;
#declare teardrop = intersection {
  merge {
    intersection {
      cylinder{
        <0,0,-teardrop_thickness> <0,0,teardrop_thickness> 1
      }
      cylinder{
        <0,0.5,-1> <0,0.5,1> 0.5
        inverse
      }
      plane{
        -x 0
      }
    }
    cylinder{
      <0,-0.5,-teardrop_thickness> <0,-0.5,teardrop_thickness> 0.5
    }
    cylinder{
      <0,0.5,-teardrop_thickness> <0,0.5,teardrop_thickness> 0.25
    }
  }
  cylinder{
    <0,-0.5,-1> <0,-0.5,1> 0.25
    inverse
  }
}

#declare rotation = -360*clock/4.0;

// White teardrop
object{
  teardrop
  texture{
    pigment{
      granite
      pigment_map{
        [0 rgbt <1,1,1,0.3>]
        [0.8 rgbt <0.5,0.5,0.5,0.3>]
        [1 rgbt <0,0,0,0.3>]
      }
    }

    finish{
      reflection 0.6
    }
  }

  interior {
    ior 1.3
  }

  photons{
    target
    reflection on
    refraction on
  }

  rotate rotation*z
  rotate -45*z
}

// Black teardrop
object{
  teardrop
  texture{
    pigment{
      granite
      pigment_map{
        [0 rgb 0]
        [0.8 rgb 0.2]
        [1 rgb 1]
      }
    }

   finish{
      reflection 0.05
    }
  }

  photons{
    target
    reflection on
    refraction on
  }

  rotate (rotation+180)*z
  rotate y*90
  rotate -45*z
}

// sky_sphere {
//   pigment{
//     //color <0.6, 0.3, 0.3>
//     color <0.2, 0.05, 0.2>
//   }
// }

plane{
  z, -5

  pigment{
    rgb 1
  }
}