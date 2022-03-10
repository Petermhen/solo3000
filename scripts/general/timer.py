import GameLogic as g


c=g.getCurrentController()
own = c.getOwner()
objList=g.getCurrentScene().getObjectList()

char_timecollide= c.getSensor("TimeCollect")
char_timecollect=char_timecollide.getOwner()


if char_timecollide.isPositive():
	timepost= char_timecollide.getHitObject()
	timepost_name= timepost.getName()
	touched_post=objList[timepost_name]
	
	own.maintimer = own.maintimer+touched_post.timepost
	touched_post.endObject()
	own.timepost_counter=own.timepost_counter+1
	


#Bullet hit subtracts time

EnemyHit_sensor=c.getSensor("EnemyHit")
MainCharacter_own=EnemyHit_sensor.getOwner()

if EnemyHit_sensor.isPositive():

	#Get the amount of time the hit received drains
	enemy_hit=EnemyHit_sensor.getHitObject()
	enemy_hit_name=enemy_hit.getName()
	enemy_hit_obj=objList[enemy_hit_name]
			
	#Subtract the amount of time that particular enemy's hit drains 
	own.maintimer=own.maintimer-enemy_hit_obj.enemy_hit
	enemy_hit_obj.endObject()
	

#Timer set
timer_amt=own.maintimer- own.timer

own.minutes=(timer_amt/60)
own.seconds =(timer_amt%60)

own.Text =( str(own.minutes) + ":" + str("%02i"% own.seconds))


#print "timer: ", own.next_level
	
#TimerDeath
game_end_act=c.getActuator("game_end")
#if (own.seconds==0 and own.minutes==0)or (own.minutes<0)or(own.seconds<0):
if timer_amt==0 or timer_amt<0:	
	g.addActiveActuator(game_end_act,1)
	
	
#Activate Stage Portal

centralpost_anim_act=c.getActuator("collect_activate_test")
portal_anim_act=c.getActuator("portal_anim")

num_of_timeposts_sensor=c.getSensor("num_of_timeposts_sensor")
num_of_timeposts_own= num_of_timeposts_sensor.getOwner()

print "timepost_counter: ", own.timepost_counter
print "num_of_timeposts: ", num_of_timeposts_own.num_of_timeposts
print "own.animplaycount: ", own.animplaycount
print "own.next_level: ", own.next_level

if (own.timepost_counter==num_of_timeposts_own.num_of_timeposts and own.animplaycount==0):
	own.next_level= 1
	g.addActiveActuator(centralpost_anim_act,1)
	g.addActiveActuator(portal_anim_act,1)
	own.animplaycount=own.animplaycount+1