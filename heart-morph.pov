// Width=1200
// Height=900
// FPS=20
// Initial_Clock=0
// Final_Clock=6

#version 3.7;

global_settings {
  assumed_gamma 1
  ambient_light 0
  photons {
    count 100000
  }
}


camera {
  location <-1,-5,1>
  look_at <-1,0,0>
  right (image_width/image_height)*x
  up z
  sky z
}

light_source {
  <10,-10,10>
  color 1
}

// Function from http://news.povray.org/povray.bugreports/thread/%3Cweb.4b9773ab2e1c2878877dd06b0@news.povray.org%3E/
#declare heart = function(x,y,z) {
  (2*y*y + x*x + z*z-1) - pow((y*y/10 + x*x),1/3)*z
}

#declare transition = (1-cos(2*pi*clock/3.0))/2;

isosurface {
  function{ (1-transition)*heart(x,y,z) + transition*heart(x,y,-z) }
  accuracy 0.001
  max_gradient 5
  contained_by{sphere{0, 1.5}}

  photons{
    target
    refraction on
  }

  // texture{
  //   pigment{
  //     rgb 1
  //   }
  // }

  pigment{
    granite
    pigment_map{
      [0 rgbt <1.0, 0.0, 0.0, 0.4>]
      [1 rgbt <0.9, 0.1, 0.1, 0.4>]
    }
  }
  interior{ior 1.3}
  normal{crackle 1 scale 0.5}
  finish{phong 0.5}
}


plane{
  z, -5

  pigment{
    rgb 1
  }
}