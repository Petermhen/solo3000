from bge import logic

# Called when the Message sensor on inventory object receives a message
def inventory():
  
  
  controller = logic.getCurrentController()
  
  owner= controller.owner
  
  messageSensor= controller.sensors['Message']
  
  if messageSensor.positive:
    
    print("inventory function triggered, bodies")
    
    # body messages received since last logic tick
    messageBodies= messageSensor.bodies
    
    # itemId= messageSensor.subject
    
    inventoryInstance= owner.groupObject
    
    for itemId in messageBodies:
    
      if itemId in inventoryInstance:
        inventoryInstance[itemId] +=1
        
        print('messageBody'+itemId +': '+str(inventoryInstance[itemId]))
        
        