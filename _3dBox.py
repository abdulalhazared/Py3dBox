"""
3dBox  alpha 1
 
DONE:
 pause mode

  game OVER status 
  halt elements iteration
  
  check analyze position to find unit adjacency
  
  clean H line when full -> new approach: remove group of items with same colors (status)
	--> random color limited to n (rgb wb)

tracking column heights is problematic because of floating y
rounding or ceiling reduce the problem but it's not complete


iterate through lines to find cluster of objects	-> check existing lists and clean them

score status and window information

TODO: 

-->COLLISION DETECTION 
    OR  
  TRYING TO INTERCEPT Y IN SUBSEQUENT RANGE UNTIL INTEGER IS REACHED
    OR
  falling only of integers...
  
   better debug mode (with cmdline params)  
  
POSITION AND MOVES RELATIVE not absolute
"""

from visual import *

scene.title = "3dBox" 
#scene.width= 400
#scene.height= 600


activeUnit = false
MIN = -4

##info = label(pos=(3,4,1))
##info2 = label(pos=(3,4,-1))


score = 0


unitList = []
haltElements = []

floorHeights = [MIN,MIN,MIN,MIN,MIN]

stopFlag = false
gameState = "playing"

colors = ["red","green","blue","black","white"]

cluster = []



def getFullRandomColor():	
	return round(random.random(),2),round(random.random(),2),round(random.random(),2)

def getLimitedRandomColor():
	
	color = ()
	
	rInt= random.randint(0,len(colors))
	rVal = colors[rInt]
	
	##print "Color ", rInt, " ", rVal
	
	if (rVal=="red"):
		color=(1,0,0)
	elif (rVal=="green"):
		color=(0,1,0)
	elif (rVal=="blue"):
		color=(0,0,1)
	elif (rVal=="black"):
		color=(0,0,0)
	elif (rVal=="white"):		
		color=(1,1,1)
		
	return color



class Area():	
	width 	= 1
	height	= 10
	length 	=  5
	unit = 1
	x=0
	y=0
	z=0
	
	def __init__(self):
		#print "New Area created"	
		box (pos=(self.x,self.y,self.z),length=self.length, height=self.height, width=self.width,opacity = 0.1) # perfect
		
	def getX(self):
		return self.x
		
	def getY(self):
		return self.y

class Unit():
	width 	= 1
	height	= 1
	length 	= 1
	x=0
	y=0
	z=0
	pos = (x,y,z)
	body = ""
	velocity = ""
	
	id= ""
	
	def __init__(self,x,y,z):
		self.x=x
		self.y=y		
		self.z=z
		self.pos=(x,y,z)
		self.velocity = vector(0,-1,0)
		
		#r,g,b = getFullRandomColor()
		r,g,b = getLimitedRandomColor()
		
		self.id = "box"+ str(len(unitList))
		self.body = box (pos=self.pos,length=self.length, height=self.height, width=self.width,color= (r,g,b) ) 
		
		#self.lab = label(pos=self.pos)
		#self.lab.text  = self.id
		
	
	def getX(self):
		return int(round( self.body.x,0)) 
		
	def getY(self):
		return int(round( self.body.y,0)) 
	
	def destroy(self):	
		#del self.body 
		self.body.visible = False
		self.id = "destroyed"
		
	def showInfo(self):
		print self.id
		print self.body.color
		

def checkUnitStatus():
	global activeUnit	
	global unitList	
	
	status = false
	#floorOrdinate = floorHeights[int (activeUnit.body.x)]
	
	
	"""
		is better ceil i.e. -4.15408   =>  -4
		because round i.e. -3.52588   =>  -4
    se l'altezza dell'oggetto 
	"""
	if (int(ceil( activeUnit.body.y,0)) == floorHeights[int (activeUnit.body.x)]):
		#print "int : ", int( activeUnit.body.y) , ' ' , floorHeights[int (activeUnit.body.x)]
		#print "round: ", int(round( activeUnit.body.y,0)) , ' ' , floorHeights[int (activeUnit.body.x)]
		status = true
	return status
	


def removeUnit(unitNumber):	
	unitList[unitNumber].destroy()	

def displayUnitInfo(unitNumber):
	unitList[unitNumber].showInfo()
	


"""
check collision with other boxes
"""
def checkCollision(x,y):
    
  for elem in haltElements:
    i,j = elem
    if x==i and y == j:
     #print "collision at " , x , " " , y , " " , i , " " , j 
     return x==i and y == j
      
def checkMovement(x,y,direction):
  
  #x increment to right or left is possible? let's see any nearby elements
  x = x + 1*direction
  return checkCollision(x,y)
  

def moveObj(obj,direction):
	step = 1
	if direction == 'up' and obj.y < 15:
		obj.y += step
	elif direction == 'down' and obj.y > 5:
		obj.y -= step
	elif direction == 'right' and obj.x < 2 and not checkMovement(int(obj.x),int(obj.y),1):
		obj.x += step
	elif direction == 'left' and obj.x > -2 and not checkMovement(int(obj.x),int(obj.y),-1):
		obj.x -= step
	

def showColumnsHeight():
  columnsValStr = ""  
  columnsValStr = str(floorHeights[0]+4) + " " + str(floorHeights[1]+4) + " " + str(floorHeights[2]+4) + " "+ str(floorHeights[3]+4) + " " + str(floorHeights[4]+4)
  
  return columnsValStr
  
def stopGame():
  for i in floorHeights:
    if floorHeights[i]>9:
      return
    
def fall(unit,floorOrdinate,increment=1):      
  #dt = 0.01*increment
  dt = 0.01*increment
  gravity = 9.8
  #gravity = 1
  
  ###print "pos ", int (activeUnit.body.x), " height ", floorHeights[int (activeUnit.body.x)]
  
  floorOrdinate = floorHeights[int (activeUnit.getX())]    
  
  ##info.text = 'x,y,x : ' + str(unit.body.x) + '  ' + str(round(unit.body.y,2)) + '  ' +  str(unit.body.z) 
  ##info2.text = '0 1 2 3 4: '  + showColumnsHeight()
  
  scoreLabel.text = 'Score: ' + str(score)
  
  """
  for index,val in enumerate(floorHeights):
    info.text += '\n fh [ '+ str(index) + ' ] :  ' + str(val)
  """
  
  bounce = 0
  maxHeight = 4
  
  #while 1 and obj.y > floorOrdinate-5:
  if unit.body.y > floorOrdinate:
      rate(50)
      #decrease y to make box fall down, time is for continous movement
      #higher or lower for velocity
      unit.body.pos = unit.body.pos + unit.velocity*dt
      

      #if negative it bounces (it changes the direction of Y vector)!!!
      if unit.body.y < floorOrdinate:
          unit.velocity.y = -unit.velocity.y
          bounce+=1
      else:
          unit.velocity.y = unit.velocity.y - gravity*dt

class Game():
	
	def setup(self):
		global scoreLabel 
		scoreLabel = label(pos=(3,1,1))
		helpLabel = label(pos=(0,-5,1))
		helpLabel.text = "Press P to pause game, ESC to quit"
		#set new area
		a1 = Area()
		self.addUnit()

		"""
		u2 = Unit(-1,4)
		u3 = Unit(0,4)
		u4 = Unit(1,4)
		u5 = Unit(2,4)
		"""
		#fall(u1.body,a1.getY()) 
		
	"""
	define user  actions
	"""
	def start(self):	
		increment = 1
		"""
		while (gameState=="pause") :	
			if scene.kb.keys: # event waiting to be processed?
				s = scene.kb.getkey() # get keyboard info		
				if s == 'k':            		    
					pause()		
		"""
		
		while (gameState!="OVER") :		
			if scene.kb.keys and gameState!="OVER": # event waiting to be processed?
				s = scene.kb.getkey() # get keyboard info		
				if s == 'left':            		    
				    moveObj(activeUnit.body,s)
				elif s == 'right':       
				    moveObj(activeUnit.body,s)
				elif s == 'down':       			    
				    increment = 2						
				elif s == 'p':				
					self.pause()
				else:
					print s
								
			
			if(len(unitList)<100) and (gameState!="PAUSE"):
					fall(activeUnit,1,increment) 				

			if checkUnitStatus():			
				unitList.append(activeUnit)			
				#print "box " , len(unitList), " stops at height: " , activeUnit.body.y , "  => ", int(round(activeUnit.body.y,0)) , " fheight : " , floorHeights[int (activeUnit.body.x)]
				floorHeights[int (round(activeUnit.body.x,0))] += 1
				#print "Height of column :" , int (activeUnit.body.x) , " is now: " , floorHeights[int (activeUnit.body.x)]
				haltElements.append ( (int(round(activeUnit.body.x,0)) , int(round(activeUnit.body.y,0))) )
				self.addUnit()
				increment=1
			
			row, eval = isBaseLineFull()
			
			if (eval):
				#print floorHeights
				removeLine(row)
				#print floorHeights
				updateFloorHeights()
				#print haltElements 
				
				
			
				
		#print "Game OVER"
		
		return score
	  

	    

	def pause(self):
		global stopFlag
		global gameState 
		
		if stopFlag:
			stopFlag = false
			gameState = "PLAYING"
		else:
			stopFlag = true
			gameState = "PAUSE"
		
		#print "Game now is in "	+ gameState
		
	def stop(self):
	  global stopFlag
	  global gameState
	  stopFlag = true
	  
	  gameState = "OVER"
	  
	  statuLabel = label(pos=(1,-2,0))
	  statuLabel.text = "GAME " + gameState 
	  
	 
	def addUnit(self):
		global activeUnit 	
		x = random.randint(-2,3)
		if(checkCollision(x,4)):
			self.stop()
		else:
			#print "--> x " + str(x) +  " "
			unit = Unit(x,4,0)	
			activeUnit = unit	
  
def joinElements(list,orientation):
	for elem in list:
		if orientation=="H":
			elem.setJoinXFlag(elem.getY())
		elif orientation=="V":
			elem.setJoinYFlag(elem.getX())
		
def removeLine(lineNumber):	
	global score
	
	for index,i in enumerate(unitList):		
		if i.getY() == lineNumber:
			i.destroy()			
			i.body.y-=1 
			
	for index,i in enumerate(unitList):		
		i.body.y-=1 	
		
	
	#tempList = [ x,y=elem for elem in haltElements if y!=lineNumber]
	global haltElements
		
	tempList = list(haltElements)
	
	for i in range(0,len(haltElements)):		
		x,y =haltElements[i]
		#print x,y
		
		if y == lineNumber:
			#print "removing " , haltElements[i] , "from " , haltElements
			tempList.remove(haltElements[i])

	 	
	haltElements = list(tempList)
	
	score+=1

  

def isBaseLineFull():	
	counter = 0
	line = -4
	for index,item in enumerate(unitList):
		#print counter , item.getY()
		if (item.getY()==line):
			counter +=1			
			
	return line, counter == 5

def updateFloorHeights():
	#print "Update Heights"
	
	for index,elem in enumerate(floorHeights):
		if elem!=0:
			floorHeights[index]-=1
	

	
def main():
	if __name__=="__main__":
		g1 = Game()
		g1.setup()
		return g1.start()	
		pass
	else:      
		pass
        
main()