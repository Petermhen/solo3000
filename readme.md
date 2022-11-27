<!-- TOC -->

- [Blender Game](#blender-game)
- [Run on Game Init](#run-on-game-init)
  - [Set script directories in .blend files](#set-script-directories-in-blend-files)
- [Logic Bricks](#logic-bricks)
  - [Set Logic Controller Module](#set-logic-controller-module)
  - [Logic Controller Debug](#logic-controller-debug)
  - [Controller States](#controller-states)
  - [Message Sensors & Actuators](#message-sensors--actuators)
- [Items](#items)
  - [Define an Item](#define-an-item)
    - [collectItem Script](#collectitem-script)
  - [Item properties](#item-properties)
  - [Item Name & ID](#item-name--id)
    - [Default item property on source object](#default-item-property-on-source-object)
    - [item property on instance object](#item-property-on-instance-object)
    - [Group item instances](#group-item-instances)
    - [Item Object Name](#item-object-name)
  - [Instancing Linked Groups](#instancing-linked-groups)
  - [Inventory](#inventory)
  - [Individual items](#individual-items)
  - [Group item](#group-item)
  - [Timepost](#timepost)
  - [Camera](#camera)
    - [Setup](#setup)
- [Character](#character)
  - [Shooting](#shooting)
- [About This Documentation](#about-this-documentation)
  - [TOC](#toc)
    - [Usage](#usage)

<!-- /TOC -->

# Blender Game

# Run on Game Init

## Set script directories in .blend files

`script_directories.blend` should be in game's root folder.

Contains script which runs 1st on runtime and adds the path to the `Scripts` folder to current .blend file path.

Import `initScriptDirectories` object from `script_directories.blend` into any .blend file that you want to access the `scripts` folder from.

# Logic Bricks

## Set Logic Controller Module

Set Logic brick set to `module`.
Value field in logic brick: `scriptName.functionName`

## Logic Controller Debug

Set `Debug` button to live reload external script on change.

No need to import the script into the internal Text Editor.

Disable `Debug` when exporting final game.

## Controller States

Each object has a set of states for all its Controllers

## Message Sensors & Actuators

Functions like calling a component and passing values to it, but as Logic bricks.

Without using messages all separate objects' sensors & actuators end up all bunched together like a giant script, rather than each object or group being a separate component whose logic is easy to follow.

# Items

Items are any collectable in the game.

## Define an Item

Items are specified in the `props.blend` file and linked to the playable game `.blend` file.

An item object must have a `near` sensor that detects when a main character is near, and triggers the `item` script.

The item script only sends a message to the Inventory object if the item source object has an `item` property.

The `inventory` object only counts the item if the item property value and/or the instance parent's name is a property on the `inventory` object.

### collectItem Script

The near sensor calls the `collectItem` function defined in `/scripts/general/items`.

## Item properties

Item must have boolean property `collected`.
This `collectItem` script sets this to `1` the specify the item as having been collected.

The `collectItem` script sets the `collected` property on any member object of item group to `1`.

An item must be an instanced group to work in game, ie. to be counted on `inventory`. The `collectItem` script checks for item object that called the script being part of an instance group, via `item.groupObject`.

## Item Name & ID

Items can be identified by any of the 3 following ways:

1. Default `item` property on source object
2. `item` property on instance object
3. Group item instances

The `inventory` object keeps any of these 3 that are assigned to an item.

Eg. Instance is added to group `timepostdoor4`, `item` property is assigned to instance with value `timepost4`, & source object has `item` property `timepost`.

The inventory object will create a property & increment the count of each of these 3 properties -(`timepostdoor4`, `timepost4`, `timepost`) everytime a timepost is collected.

### Default item property on source object

The default `item` property on the original source item. If this property is missing the item is identified by the name of its gameObject. Eg. item property: timepost. This allows multiple item objects to count as the same item.

Specified on the `MessageToCountItem` actuator.

Eg. different health item objects with different designs that each add different amounts of health.

### item property on instance object

Add an `item` property to the instance object.

Specified on the `MessageToCountItemInstance` actuator.

Eg. 3 timepost instances have an `item` property added & set to `timepostdoor3`. Each time the `timepost` item is collected, the `timepostdoor3` property on the `inventory` object is incremented by 1.

### Group item instances

Add the of the item's group to their own group.
This is preferred to #2 as the items are identified by their group name, which is unique across all scenes.

Specified on the `MessageToCountItemGroup` actuator.

This prevents the error such as Eg. assigning 3 'timepost' items's `item` property to `timepostdoor6`, which triggers 'door4' to open when collected. But `timepostdoor6` was assigned in a previous level & 3 items collected already, thus the door defaults to open because of this id conflict. Grouping the item instances prevents this.

### Item Object Name

The item object's name is used to identify the item in logic bricks, therefore if the item name is changed the in the Outliner the name must be changed in the item's relevant logic bricks also.

The object's name is used as the item ID to provide a simple way for ensuring that the item ID is always unique across all scenes in the .blend file.

## Instancing Linked Groups

Any scripts run on the source group objects to all instances & original object.

To apply to the individual instanced group that called the script, scripts on source objects can select the instanced object via `owner.groupObject` and `owner.groupObject.groupMembers`.

## Inventory

Inventory object is a child of the Character object. 

This ensures that all inventory counts are transferred between levels, once the same character group is transferred. 

The `inventory` script checks for item counts in two ways:

### On inventory object 

### On inventory object's parent's instance 
For counting 

~~
The item count is tracked in the `inventory` object, which is in `props.blend`

This object must be linked within any .blend file where items are being collected.

The instanced `inventory` group must have the properties specified on it that are to be counted.

The subject of the message sent to the Inventory object must be the same as a property on the object.
~~

## Individual items

Standard items. The number of items collected is tracked on the `inventory` object. Eg. ammo.

## Group item

When an item object is linked from `props.blend` to the playable .blend file, if the linked item is added to a group, it will be counted as a group on the `inventory` object.

Eg. The individual `timepost` item can be added to a group named `timepostsForDoor1`, which specifies 3 timeposts which must be collected to open `door 1`.

These number of timeposts in the group `timepostsForDoor1` would be tracked in the `inventory` object. When the count reaches 3 the `door1` open animation would be played.

## Timepost

The timepost group has to be instanced for it to work, as the instance's `groupObject`'s members are checked for the `collected` property.

## Camera

### Setup

`cameraRotateLeftRight` is vertex parented to character, so it doesn't get character's rotation, only translation.

# Character

## Shooting

Activated on left mouse button press.

Position of horizon convergence point from crosshair is calculated.

Horizon convergence point depends on how high or low your view is.

Lower view has smaller convergence point (can't see as far)

Higher view has farther point (can see further)

Taking horizon convergence point from standard 6 ft eye level, it's a distance of 3.1 miles, or 16368 ft. Have to convert this to blender units.

## Fire Rate 
Full auto weapons: 10 rounds per second. Same as ak47 rifle

Semi auto: 2 rounds per second.

# Enemies
## Sight 
Using Radar sensor to define cone that specifies area in which enemy can detect player.

## States 
### Patrol 
Move through defined patrol waypoints in order that they're listed.

Chase player when spotted. If player gets far enough away then go back to patrol.

#### Waypoints 
The `waypoints` can be any object that's a child of the linked enemy instance. The name of the object must start with `waypoint`. The enemy moves to each waypoint according to the order in which they're arranged in the Outliner.

### Seek 
Seek out player whereever he is on map. 
Make it intermittent, unless player is within line of sight. Stop and take breaks, like switching to guard state momentarily.


### Guard 
Stay in one spot & turn side to side. 

Chase player when spotted. If player gets far enough away then go back to patrol.

## Instances 
Properties that uniquely identify each enemy, like enemy's current `life`, can be defined on each instance, or can be left as the default property as defined on the source of that instance.
Eg. default `life` property on `Patroller` enemies is `30`.

Only an instance of the original enemy object works, as the `init` function assumes that it's running on an instance, ie. `owner.groupObject != None`

# Spawn Point 
Code setup to only work with instances of the spawn point 

Optional parameters:
1. max: max number of enemies to spawn. Defaults to 15
2. interval: time in seconds between spawning enemies. Defaults to 120


# Benchmarks 
## BASELINE
empty scene: balanced 60fps 

pulse true on, 1 obj moving 0.05 in x axis every logic tic  
  balance: 60fps

## 2000 objects: Always sensor on obj1. Connected to obj2 that moves obj 0.05 each logic tic on x axis

### w/ pulse true on
  start: 22fps
  low: 19fps 
  balanced out after 15 secs: 20fps 

### w/ pulse off
  ditto above 

### w/ pulse on, skip 30 frames, tap on 
  objects moving 0.05 on x axis, 2x per second, rather than 60x per second.
  constant 60fps 

## w/ pulse on, skip 4 frames, tap on, move 0.2 in x axis, or 4x amount, so object moves same amount per second, but in larger chunks every 4 logic tics
  Appears slightly less smooth

  constant 41fps 

## always sensor obj1 connected to property actuator that sets property to 1 on every logic tic on obj2 
  ### pulse on, skip= 0, tap off 
    balanced: 59

## 2k objects. Always sensor pulse true on obj1, connected to python script on obj2 that sets activates motion actuator on obj2 every logic tic 
    start: 16
    low: 12 
    balanced: 13 

## 2k objects. Always sensor pulse false on obj1, connected to python script on obj2 that activates motion actuator on first logic tic only. Script doesn't fire after
    start: 22fps
    low: 19fps 
    balanced out after 15 secs: 20fps 

    Same as logic brick only setup w Always sensor pulse set to true to run on each logic tic.

##  2k objects. Always sensor pulse true on obj1, connected to python script on obj2 that activates motion actuator on every logic tic, on each tic checks property that has it only only activate actuator on 1st logic tic
    start: 16
    low: 12 
    balanced: 13 

    Just running script every logic tic has big hit on framerate regardless. 


##  2000 objects: message sensor connected to motion actuator that moves obj 0.05 each logic tic on x axis, always sensor connected message actuator on obj1
  always sensor positive pulse MUST be on for object to move on each logic tic. Message sensor doens't need positive pulse 

  This setup results in ~ 3 to 4 fps less than two directly connected objects for 2000 objects. 
  .4fps for 200 objects. And that's if they're all firing at the same time! 

### 2k objects, always & message sensor disabled 
    balanced: 57fps 

  ###  Message sensor +ve pulse on, actuator sending message to specified object, not broadcasting
      start: 17fps 
      low: 13fps 
      balanced: 14fps 
    
  ###  message sensor pulse off 
      ditto above 

  ###  Message sensor +ve pulse on, actuator broadcasting message 
      start: 17fps 
      low: 13fps 
      balanced: 14fps 

      Basically no difference, just have to contend with possible naming conflicts between other broadcasted messages.
    

  ###  always sensor & message sensor set to skip 4 frames & tap on. Motion set to 0.2 in x axis. Same amount of movement, but larger increments every 4 logic tics 
      start: 39 
      low: 34 
      balanced: 37

  ##  2k objects. On obj1 Always sensor w pulse off, sends message to obj2. Obj 2 message sensor pulse off, sets property on obj2. Property sensor w pulse off triggers motion actuator on object every logic tic 
      low: 11
      balanced: 12.5

      Why? Every additional sensor equates to more checks to run each logic tic. The message sensor 

  ##  2000 objects: always sensor connected message actuator on obj1, message sensor connected to property actuator that sets property to 1 on every logic tic 

  ### always & message sensor +ve pulse on, skip 4 logic tics , always sensor tap on
        balanced: 57

  ### same, skip= 0, tap off 
        balanced: 51

      always & message sensor +ve pulse on, only send message on 1st logic tic 
        balanced: 58

  ## CONCLUSIONS:
    Pulse mode on/off makes no difference if controller is activated each logic tic. 

    less sensors the better regardless of the setup. 

      sensor.active 
        deactivating unused sensors via python script should increase performance 

      OR use states, within which ONLY the sensors that are needed for the object's current functionality will be active.

      Unneeded message sensors as opposed to direct connection will start to add up. 

    Direct connections between objects faster than message sensors 
      but requires 100s of messages at same time to affect fps on my system.
      So minimise but use where relevant such as between separate Collections/groups.

    SKIPPING logic tics on sensors can make a significant difference in performance 

# About This Documentation

## TOC

Auto generated Table of Contents with VSCode Plugin `Auto Markdown TO`

### Usage

Install plugin in VSCode

In .md file, Right click -> "Auto Markdown TOC Insert/Update TOC"

On saving file TOC is auto updated
