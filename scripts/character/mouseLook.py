#:::::::::::::::::::::::::::::::::::::::::#
#	        Capped Mouse Look             #
#:::::::::::::::::::::::::::::::::::::::::#
#Tutorial for using MouseLook.py by Clark Thames can be found at
#    www.tutorialsforblender3D.com

# - Capped Mouselook Script thanks to B3D00

import bge
from bge import logic 

def mouseLook():

  import Rasterizer as r

  import bge
  from bge import logic as GameLogic
  import GameKeys

  controller = GameLogic.getCurrentController()
  owner = controller.owner

  # bge.render.showMouse(True)

  #if hasattr(owner, 'x')==0:
  #    owner.x=0.0

  mouse=controller.sensors["Mouse Look"]
  lmotion=controller.actuators["leftright"]
  wmotion=controller.actuators["updown"]
      
  if mouse.positive:
    sens=0.0035        #leftright  sensitivity
    sens2=0.0015    #updown sensitivity

    posx=(bge.render.getWindowWidth()/2-mouse.position[0])*sens
    posy=(bge.render.getWindowHeight()/2-mouse.position[1])*sens2

    #        top limit           bottom limit
    # if owner["x"]<=-.8 and posy<0 or owner["x"]>=.5 and posy>0:
    #     posy = 0.0
    # owner["x"]+=posy

    lmotion.dRot=[0,0,posx]
    wmotion.dRot=[posy,0,0]
    #wmotion.dRot=[0,0,0]
    print('mouselook pos: posx:' + str(posx) + ' posy: '+str(posy))
    

      
  # else:
  #   lmotion.dRot=[0,0,0]
  #   wmotion.dRot=[0,0,0]

  #   print('mouselook neg:')
      
  controller.activate(wmotion)
  controller.activate(lmotion)
  # controller.deactivate(wmotion)
  # controller.deactivate(lmotion)
  
    #Set cursor to centor of viewport on logic tick after each movement
  bge.render.setMousePosition(int(bge.render.getWindowWidth()/2),int(bge.render.getWindowHeight()/2))
  # bge.render.setMousePosition(0,0)

  #r.setMousePosition(r.getWindowWidth()/2,r.getWindowHeight()/2)
  
  
  
import bge, math
from bge import render
from mathutils import Vector

def mouseLook2():

  cont = bge.logic.getCurrentController()
  own = cont.owner

  # Get the child object named "Camera"
  # camera = own.children['Camera']

  # Props
  cap = True
  capLow = 20
  capHigh = 120

  # Get the sensor "Mouse"
  mouse = cont.sensors ["Mouse Look"]

  # sensib = Property on this object named "Sensibilite"
  sensib = own['sensitivity']

  # Get the center of the screen
  x = render.getWindowWidth()//2
  y = render.getWindowHeight()//2

  screen_mid = (x,y)

  # center = Center of the screen
  center = Vector(screen_mid)

  # Get the position of the mouse
  mouse_position = Vector(mouse.position)

  # Define the rotation that should be made
  offset = (mouse_position-center)*-sensib*0.0002

  if mouse.positive: #This part has changed!
      # Get the rotation of the camera
      Camrot = own.localOrientation.to_euler()
      Camrotx = math.degrees(Camrot[0])
      print(Camrotx)

      # Check if new rotation value would be too high
      if Camrotx + offset.y > capHigh and cap == True:
          # Choose offset.y so that: Camrotx + offset.y = capHigh
          offset.y = math.radians(capHigh - Camrotx)

      # Check if new rotation value would be too low
      elif Camrotx + offset.y < capLow and cap == True:
          offset.y = math.radians(capLow - Camrotx)

      # Apply the rotation the the camera
      own.applyRotation(( offset.y, 0, 0), True)

  # Apply the horizontal rotation to the player/parent object
  own.applyRotation((0, 0, offset.x), True)

  # Reset the mouse position
  render.setMousePosition(x,y)

def activeCamera():
  scene = logic.getCurrentScene()
  cam = scene.objects['Camera.002']
  
  print('cam:'+ cam.name)
  
  scene.active_camera = cam