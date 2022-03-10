from bge import logic

# Set property to specified value on members of linked instance group that have specified property
#params:
#myGameObject: source object of linked instance group, as returned by raySensor.hitObject, etc
def setPropertyOnInstanceGroupMembers(myGameObject,propertyName,propertyValue):
   
  # if object is really a group instance then get its group instance object 
  if myGameObject.groupObject:
    print("groupObject:"+ myGameObject.groupObject.name)
    
    print('groupMember length: ' + str(len(myGameObject.groupObject.groupMembers)))
    
    # Get the objects in the instanced group
    for groupMember in myGameObject.groupObject.groupMembers:
      print('groupMember: '+ groupMember.name)
      
      # Get main item object
      if propertyName in groupMember:
        groupMember[propertyName]=propertyValue
        print('property: '+ str(groupMember[propertyName]))

def addToPropertyOnInstanceGroupMembers(myGameObject,propertyName,propertyValue):
   
  # if object is really a group instance then get its group instance object 
  if myGameObject.groupObject:
    print("groupObject:"+ myGameObject.groupObject.name)
    
    print('groupMember length: ' + str(len(myGameObject.groupObject.groupMembers)))
    
    # Get the objects in the instanced group
    for groupMember in myGameObject.groupObject.groupMembers:
      print('groupMember: '+ groupMember.name)
      
      # Get main item object
      if propertyName in groupMember:
        groupMember[propertyName]=groupMember[propertyName]+propertyValue
        print('property: '+ str(groupMember[propertyName]))
