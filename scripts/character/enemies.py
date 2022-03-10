import GameKeys,random
from bge import logic  
from mathutils import Vector

def init():
    controller = logic.getCurrentController()
    owner = controller.owner
    scene= logic.getCurrentScene()

    state2= controller.actuators["State2"]

    #Actuators:
    motion = controller.actuators["motion"]
    pursue = controller.actuators["pursue"]

    # Define properties that uniquely identify each enemy instance 
    if "life" in owner.groupObject:
        #Replace default "life" property on source object specific to linked instance
        owner["life"]=owner.groupObject["life"]
        owner["totalLife"]=owner.groupObject["life"]

    if owner.groupObject["type"]=="pursue":
        controller.activate(state2)
        
    #Get waypoints for current enemy & set current waypoint
    elif owner.groupObject["type"]=="patrol":

        print("set waypoints")
        #Name of each waypoint 
        waypoints=[]

        # Waypoints for enemy are children of empty with name enemyNameWaypoints
        # objects in instanced enemy
        print("enemy groupobject children: ")
        for child in owner.groupObject.children: #name+"Waypoints"].children:
            print(child.name)
            if "waypoint" in child:
                waypoints.append(child.name) 

        waypoints.sort()

        owner["waypoints"]= " ".join(waypoints)
        
        owner["currentWaypoint"]= waypoints[0]

        print("waypoints:")
        print(owner["waypoints"])
        
        #Set object for enemy to track towards
        pursue.object= scene.objects[owner["currentWaypoint"]]

        controller.activate(pursue)
        controller.activate(motion)

   

def setPlayerTrack():
    controller = logic.getCurrentController()
    owner = controller.owner
    scene= logic.getCurrentScene()

    trackPlayer= controller.actuators["TrackPlayer"]

    trackPlayer.object= scene.objects["Main_character"]

def circleRandom():
    controller = logic.getCurrentController()
    owner = controller.owner
    scene= logic.getCurrentScene()

    randomDirection= random.choice([-1,1])

    lateralMotionActuator= controller.actuators["LateralMotion"]

    lateralMotionActuator.dLoc=Vector((0.08*randomDirection,0,0))



def receiveHit():
    print("receiveHit")
    controller = logic.getCurrentController()
    
    hitSensor= controller.sensors["Hit"]

    # messageActuator= controller.actuators["Message.001"]

    if hitSensor.positive:

        owner = controller.owner
        scene= logic.getCurrentScene()
        
        owner["life"]= owner["totalLife"]- owner["hits"]

        # Set life of the group instance
        # owner["life"]= owner["life"]- totalHits

        # owner.groupObject["life"]= owner.groupObject["life"]- totalHits

        # if (owner.groupObject["life"]<=0):
        #     controller.activate(messageActuator)
        #     owner.groupObject.endObject()

def patrol():
    controller = logic.getCurrentController()
    owner = controller.owner
    scene= logic.getCurrentScene()

    # enemyId= owner.groupObject["id"]

    #Sensors:
    nearWaypoint= controller.sensors["NearWaypoint"]
    # playerRadar = controller.sensors["PlayerRadar"]
    # nearPlayer = controller.sensors["NearPlayer"]

    #Actuators:
    motion = controller.actuators["motion"]
    pursue = controller.actuators["pursue"]

    #Set next waypoint 
    if owner["currentWaypoint"] and nearWaypoint.positive and nearWaypoint.hitObject.name==owner["currentWaypoint"]: 
        waypoints= owner["waypoints"].split() 

        print("set next waypoint")

        try:
            currentWaypointIndex= waypoints.index(owner["currentWaypoint"])

            # Set to next item in list, or reset to start of list 
            if currentWaypointIndex<len(waypoints)-1:
                owner["currentWaypoint"]= waypoints[currentWaypointIndex+1]
            else:
                owner["currentWaypoint"]= waypoints[0]

            #Set object for enemy to track towards
            pursue.object= scene.objects[owner["currentWaypoint"]]

            controller.activate(pursue)
            
        except:
            pass

def initSpawnPoint():
    controller= logic.getCurrentController()
    owner= controller.owner

    #Overwrite default values if explicitly defined
    if "max" in owner.groupObject:
        owner["max"]= owner.groupObject["max"]

    if "interval" in owner.groupObject:
        owner["interval"]= owner.groupObject["interval"]

    if "delay" in owner.groupObject:
        owner["delay"]= owner.groupObject["delay"]

    delaySensor= controller.sensors["Delay"]

    countPropertySensor= controller.sensors["CountProperty"]

    stateActuator= controller.actuators["State"]

    #Set max spawn value 
    countPropertySensor.value= str(owner["max"])

    #Set spawn interval in seconds
    delaySensor.skippedTicks= owner["interval"]*60

    #set to delay before first enemy is spawned
    delaySensor.delay= owner["delay"]*60

    #Switch spawn point to active state
    controller.activate(stateActuator)

    print("init spawn")
    print("max: "+ str(owner["max"]))
    print("interval: "+ str(owner["interval"]))

