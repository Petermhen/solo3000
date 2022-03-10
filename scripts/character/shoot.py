from bge import logic
import mathutils
from general import addToPropertyOnInstanceGroupMembers

def crosshair():
  controller = logic.getCurrentController()

  owner = controller.owner

  scene = logic.getCurrentScene()

  sceneObjects = scene.objects

  raySensorForAttackable= controller.sensors['Radar']

  shootTriggeredMessage= controller.sensors['ShootTriggeredMessage']

  hitMessage= controller.actuators['HitMessage']

  if raySensorForAttackable.positive and shootTriggeredMessage.positive:

    #Set player rotation to camera rotation 

    camera= sceneObjects['Camera']

    cameraWorldOrientationEuler= camera.worldOrientation.to_euler()

    player= sceneObjects['Main_character']

    playerWorldOrientationEuler= player.worldOrientation.to_euler()

    print("cameraWorldOrientation:")
    print(cameraWorldOrientationEuler)

    print("playerWorldOrientation")
    print(playerWorldOrientationEuler)

    #Set hit amount on enemy
    addToPropertyOnInstanceGroupMembers(raySensorForAttackable.hitObject,"hits",owner["weaponStrength"])

    #Rotate to direction of camera
    playerWorldOrientationEulerRotatedToCamera= mathutils.Euler((playerWorldOrientationEuler.x,playerWorldOrientationEuler.y,cameraWorldOrientationEuler.z))

    playerWorldOrientationMatrixRotatedToCamera= playerWorldOrientationEulerRotatedToCamera.to_matrix()

    player.worldOrientation= playerWorldOrientationMatrixRotatedToCamera

    shootMessageToArmature= controller.actuators['ShootMessageToArmature']

    shootMessageToGun= controller.actuators['ShootMessageToGun']
    shootMessageToShells= controller.actuators['ShootMessageToShells']

    controller.activate(shootMessageToArmature)

    controller.activate(shootMessageToGun)
    controller.activate(shootMessageToShells)

    # player.worldOrientation= ((0,0,0),(0,0,0),(0,0,0))

    
    # controllerObject['objectInCrosshairs']= True
    # controllerObject['xPosition']=raySensor.



    # addDecalActuator= controller.actuators["AddDecal"]
    
    # controller.activate(addDecalActuator)

    bulletHit= sceneObjects["bulletHit"]

    bulletHit.worldPosition= raySensorForAttackable.hitPosition
    bulletHit.localPosition= [bulletHit.localPosition.x,bulletHit.localPosition.y,bulletHit.localPosition.z+0.05]

    print('hit normal:')
    print(raySensorForAttackable.hitNormal)

    #Set decals
    # if not "noDecals" in raySensorForAttackable.hitObject:
    #   decalGameObject= scene.addObject("bulletDecal","bulletHit")
    #   decalGameObject.alignAxisToVect(raySensorForAttackable.hitNormal)
    #   decalGameObject.setParent(raySensorForAttackable.hitObject)
    