#:::::::::::::::::::::::::::::::::::::::::#
#	         Camera Collision             #
#:::::::::::::::::::::::::::::::::::::::::#

def cameraCollision():

  from bge import logic as GameLogic
  import GameKeys

  controller = GameLogic.getCurrentController()
  owner = controller.owner

  objList = GameLogic.getCurrentScene().objects

  cam_par = objList["Camera_Parent"]
  cam_pos = objList["Camera_Position"]
  cam_pivot = controller.owner

  ob,hit,normal = cam_pivot.rayCast( cam_pos, cam_pivot, 0.0, "wall", 0, 1)

  if hit != None:
    cam_par.worldPosition=hit

  else:    
    cam_par.worldPosition=cam_pos.worldPosition	

  #----[ notes ]--------------------------------------------------------------------
  #
  # This script sends a ray from the "Camera_Pivot"
  # to the "Camera_Position" empty,
  # if the ray hits a wall property the camera is moved to the hit position.
  # if the ray does not hit the wall, the camera is moved
  # to the "Camera_Position" empty.
    
  # The original idea was from ST150's camera collision setup
  # www.blending-online.co.uk