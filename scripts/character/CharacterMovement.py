import GameKeys
from bge import logic as GameLogic

# Character Moves

# To Allow for easily toggling prints on or off
def printLine(line):
  if shouldPrint==True:
    print(line)

shouldPrint= False

def playerMove2():
  
  cont = GameLogic.getCurrentController()
  own = cont.owner 

  objList = GameLogic.getCurrentScene().objects
  front_tget = objList["front"]
  back_tget = objList["back"]
  left_tget = objList["left"]
  right_tget = objList["right"]
  front_right_tget = objList["front_right"]
  front_left_tget = objList["front_left"]
  back_left_tget = objList["back_left"]
  back_right_tget = objList["back_right"]

  #:::::::::::::::::::::::::::::::::::::::::#
  #		      S E N S O R S               #
  #:::::::::::::::::::::::::::::::::::::::::#

  forward=cont.sensors["key_up"]
  backward=cont.sensors["key_down"]
  turn_left=cont.sensors["key_left"]
  turn_right=cont.sensors["key_right"]
  dash=cont.sensors["key_lShift"]

  ground_test=cont.sensors["ground_test"]

  platform_test=cont.sensors["platform_test"]


  #:::::::::::::::::::::::::::::::::::::::::#
  #	        A C T U A T O R S             #
  #:::::::::::::::::::::::::::::::::::::::::#

  #Move Forward - Move Backward
  moves = cont.actuators["moves"]

  # Track to empty
  direction = cont.actuators["direction"]

  # Stop Moves on Y axis
  stop_y = cont.actuators["stop_moves_y"]


  shootMotion= cont.actuators["ShootMotion"]

  #--------[ Settings ]-------------------------------------------------

  speed_fw = 4				#Forward
  ForceLimitYMax_value=40	#LimitYMax
  ForceLimitYMin_value=0	#LimitYMax

  # Dash
  speed_dash = 10			#Forward
  ForceLimitYMax_Dash_value=55	#LimitYMax			
  ForceLimitYMin_Dash_value=0	#LimitYMax			

  # Shooting Walk Speed
  shootingWalkSpeed = 0		#Forward
  ForceLimitYMaxShootingWalk=500	#LimitYMax			
  ForceLimitYMinShootingWalk=0	#LimitYMax			


  #--------[ Variables ]------------------------------------------------

  up_key=0
  down_key=0
  left_key=0
  right_key=0
  Z=0
  Q=0
  S=0
  D=0

  ForceLimitXMax=0
  ForceLimitXMin=0
  ForceLimitYMax=0
  ForceLimitYMin=0
  ForceLimitZMax=0
  ForceLimitZMin=0


  move_state=0
  walk = 0

  target=""

  printLine("character script")

  #--------[ Run test ]-------------------------------------

  # for key in cont.sensors:
  #   print(cont.sensors[key.name])

  shootingMessage=cont.sensors["ShootingMessage"]

  if dash.positive and own["moving"]!=0:
    printLine("running")
    speed_fw = speed_dash							#Forward
    ForceLimitYMax_value=ForceLimitYMax_Dash_value	#LimitYMax	
    ForceLimitYMin_value= ForceLimitYMin_Dash_value
    own['running']=1
   
  else:
    own['running']=0

  print('shootingMessage:' +str(shootingMessage.positive))

  # if shootingMessage.positive:
  #   speed_fw = shootingWalkSpeed							#Forward
  #   ForceLimitYMax_value=ForceLimitYMaxShootingWalk	#LimitYMax	
  #   ForceLimitYMin_value=ForceLimitYMinShootingWalk

  #--------[ Ground collision test ]-------------------------------------

  if ground_test.positive:
    own["grounded"]=1
  else:
    own["grounded"]=0



  #--------[ Moving forward ]--------------------------------------------

  if forward.positive and turn_left.positive:
  #	print "Moving forwardLeft"
    up_key = 1
    left_key = 1
    move_state = 1
    
    direction.object=front_left_tget

  elif forward.positive and turn_right.positive:
    printLine("Moving forwardRight")
    up_key = 1
    right_key = 1
    move_state = 1
    
    direction.object=front_right_tget
    

  elif forward.positive:
    printLine("Moving forward")	
    up_key=1
    move_state=1
    
    direction.object=front_tget
    


  #--------[ Moving backward ]---------------------------------------------

  elif backward.positive and turn_left.positive:
    
    down_key=1
    left_key=1
    move_state=2
    
    direction.object=back_left_tget
    
  elif backward.positive and turn_right.positive:
    
    down_key=1
    right_key=1
    move_state=2
    
    direction.object=back_right_tget
    
    
  elif backward.positive:
    
    down_key=1
    move_state=2
    
    direction.object=back_tget



  #--------[ Moving to the left and right ]------------------------------
    
  elif turn_left.positive:
  #	print "Turning left"
    left_key=1
    move_state=3
    
    direction.object=left_tget


  elif turn_right.positive:
  #	print "Turning right"
    right_key=1
    move_state=3
    
    direction.object=right_tget
    



  #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
  # Set some variables before activating/deactivating actuators
    
  if move_state==0:
    own["message"]="Not Moving"
    own["moving"]=0
    
  else:
    own["message"]="Moving"
    own["moving"]=1
    
    print('speedfw: '+str(speed_fw))
    # Moves
    walk = speed_fw
    ForceLimitYMax=ForceLimitYMax_value
    ForceLimitYMin=ForceLimitYMin_value
    

    
  moves.linV=[0, walk, 0]
  moves.forceLimitY=[ForceLimitYMin, ForceLimitYMax, True]
  #moves.forceLimitZ=[ForceLimitZMin, ForceLimitZMax, True]
    
  

  #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::		
  # The Player is not moving

  if move_state==0: # or shootingMessage.positive:

    # Deactivate moves	
    cont.deactivate(moves)
    
    # Activate stop_y
    cont.activate(stop_y)
    
    # Don't track to empty
    cont.deactivate(direction)
    cont.deactivate(shootMotion)

  # The Player is moving	
  else:	
    if shootingMessage.positive:
      cont.activate(shootMotion)
      cont.deactivate(stop_y)
      cont.deactivate(moves)

    else: 
      printLine("movestate not = 0")
      # Deactivate stop_y
      cont.deactivate(stop_y)

      cont.deactivate(shootMotion)

      # Activate moves
      
      cont.activate(moves)

      cont.activate(direction)
      
      # playerArmature= objList["Armature"]
      # if playerArmature["shootingAnimation"]>14 or playerArmature["shotAlready"]==False:
      
      #   cont.activate(moves)

      #   cont.activate(direction)
      
      # else:
      #   cont.deactivate(moves)
      #   cont.deactivate(direction)


      
    