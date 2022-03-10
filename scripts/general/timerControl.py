from bge import logic

 #parent should be the Text(timer) object

class timer():
    def __init__(self,controller):
        self.controller=controller
        self.owner=controller.owner
            
        self.owner['scriptCount']+=1
        
        if self.owner['scriptCount']==1: 
           #timerType: countDown, countUP
            if self.owner['startingTime']>self.owner['endTime']:
                self.owner['timerType']="countDown"
            elif self.owner['startingTime']<self.owner['endTime']:
                self.owner['timerType']="countUp"        
                
            self.owner['turnOff']=False #declare vars
            self.owner['currentTime']=self.owner['startingTime']
        
    def run(self):    
        if self.owner['timerType']=="countDown" and self.owner['turnOff']==False:
            self.countDown()
        elif self.owner['timerType']=="countUp" and self.owner['turnOff']==False:
            self.countUp()
            
    def countDown(self):
        if self.owner['currentTime']>self.owner['endTime']: #and self.owner['scriptRun']>=1: #run count from 2nd logic tick. Seems game only really "starts" then.
            self.owner['currentTime']=self.owner['currentTime']-self.owner['increment']

        else:
            self.owner['currentTime']=self.owner['endTime']
            self.owner['turnOff']=True 
               
        self.updateTextDisplay()
    
    def countUp(self):
        if self.owner['currentTime']<self.owner['endTime']: #and self.owner['scriptRun']>=1: #run count from 2nd logic tick. Seems game only really "starts" then.
            self.owner['currentTime']=self.owner['startingTime']+self.owner['increment']

        else:
            self.owner['currentTime']=self.owner['endTime']
            self.owner['turnOff']=True 
               
        self.updateTextDisplay()
        
    def updateTextDisplay(self):    
        self.owner['Text']=str(self.owner['currentTime'])
        #~ import pdb; pdb.set_trace()
     
    def resetTimer(self):
        #~ self.owner['scriptCount']=0
        pass 

def main():
    from bge import logic
    controller=logic.getCurrentController()
    owner=controller.owner

    # for key in controller.sensors:
    #     print(controller.sensors[key.name])

    timepostMessageSensor= controller.sensors['TimepostCollectMessage']
    


    if timepostMessageSensor.positive:
        for body in timepostMessageSensor.bodies:
            owner['currentTime']+=30
        
    # print("Properties:")
    # for key in owner.getPropertyNames(): 
    #     print('prop: '+key)

    owner['scriptCount']+=1
    
    if owner['scriptCount']==1: 
        #timerType: countDown, countUP
        if owner['startingTime']>owner['endTime']:
            owner['timerType']="countDown"
        elif owner['startingTime']<owner['endTime']:
            owner['timerType']="countUp"        
            
        owner['turnOff']=False #declare vars
        owner['currentTime']=owner['startingTime']

    timerObj=timer(controller)
    timerObj.run()

    # print('tmr: ',owner['currentTime'])

# To make text high resolution
def initiateGameText():
        
    print('timerscript2')

    # owner.resolution = 8.0 # resolution is normaly 1.0 / 72 dpi
    
