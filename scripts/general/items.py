from bge import logic
from general import setPropertyOnInstanceGroupMembers

def initiateItem():
  
  cont=logic.getCurrentController()
  own=cont.owner 
  
  print('group: '+own.groupObject.name)
  print('group: '+str(own.groupObject['prop']))
  

def timepostCollected():
  controller=logic.getCurrentController()
  
  owner=controller.owner
  
  # Get instance group 
  groupInstance= owner.groupObject  
  

# Set properties and actuators to collect item when main character is near item. Item must be an instanced group.
def collectItem():
  controller=logic.getCurrentController()
  
  owner=controller.owner 
  
  # Only run item functionality if item object that called script is part of an instance group.
  if owner.groupObject:
    
    # Name of property that identifies item on source object and on instance object.
    # itemIdName= 'item'

    
    # check that 'collected' property exists hasn't already been set to 1 meaning item was collected already.
    if 'collected' in owner and owner['collected'] == 0:
      #item not collected 
      
      print("owner name:"+ owner.name)
      
      # Set 'collected' property that exists on all members of instance group to 1
      setPropertyOnInstanceGroupMembers(owner, 'collected',1)
      
      
      #Send messages to inventory object to count the item by its 'item' id property on source object.
      if 'item' in owner:
        
        #Keep Count of the general item. Eg. bullet, rather than specific group "9mm bullets
        # if actuator exists 
        if 'MessageToCountItem' in owner.actuators:
          countItemMessageActuator=owner.actuators["MessageToCountItem"]
          
          countItemMessageActuator.body= owner['item']
          
          controller.activate(countItemMessageActuator)
          controller.deactivate(countItemMessageActuator)
          
          
        # Send message to inventory object to count the instnaced item by its instance name, if 'item' property is on instance
        
        
        # Send message to inventory object to count the instanced item by its instance group name, if the instance's group has 'item' property

        #-----------------------------------------------------------#
        # For item 
        itemInstance= owner.groupObject
        
        #Count item instance group 
        # itemInstanceParent= itemInstance.parent
      
        print('itemInstance: ' +itemInstance.name)
        # print('itemInstance parent: ' +itemInstanceParent.name)
        
        #Send item instance parent's name as a message to Inventory object
        
        print('instanceGroup: ')
        


        #Keep count of the item's specific group. Eg. "9mm bullets"

        # if actuator exists 
        if 'MessageToCountItemGroup' in owner.actuators:
          countItemGroupMessageActuator=owner.actuators["MessageToCountItemGroup"]
          
          # Set message to the name of the instance 
          # countItemGroupMessageActuator.body= itemInstanceParent.name

          # Set message to the value of the "item" property 
          countItemGroupMessageActuator.body= itemInstance["item"]
          
          controller.activate(countItemGroupMessageActuator)
          controller.deactivate(countItemGroupMessageActuator)
        
        #-----------------------------------------------------------#
          
    
    # countItemInstanceMessageActuator=owner.actuators["MessageToCountItemInstance"]
    
    # countItemGroupMessageActuator=owner.actuators["MessageToCountItemGroup"]
    
    