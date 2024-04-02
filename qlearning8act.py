import numpy as np
import sys
import cv2 as cv2
import time

#=================================================================================
#draw blank image

start_time = time.time()

row = int(sys.argv[2])
column = int(sys.argv[1])

height, width = 640, 640
b, g, r = 0xFF, 0xFF, 0xFF  # orange
image = np.zeros((height, width, 3), np.uint8)
image[:, :, 0] = b
image[:, :, 1] = g
image[:, :, 2] = r

#draw rectangle
#iact = np.zeros((40, 40, 3), np.uint8)
iact0 = cv2.imread('act1.jpg')
iact0 = cv2.resize(iact0,(40,40))

iact1 = cv2.imread('act2.jpg')
iact1 = cv2.resize(iact1,(40,40))

iact2 = cv2.imread('act3.jpg')
iact2 = cv2.resize(iact2,(40,40))

iact3 = cv2.imread('act4.jpg')
iact3 = cv2.resize(iact3,(40,40))

iact4 = cv2.imread('act5.jpg')
iact4 = cv2.resize(iact4,(40,40))

iact5 = cv2.imread('act6.jpg')
iact5 = cv2.resize(iact5,(40,40))

iact6 = cv2.imread('act7.jpg')
iact6 = cv2.resize(iact6,(40,40))

iact7 = cv2.imread('act8.jpg')
iact7 = cv2.resize(iact7,(40,40))

font = cv2.FONT_HERSHEY_SIMPLEX
#org = (50, 50)
fontScale = 0.5
color = (255, 0, 0)
thickness = 1

for y in range(row):
  for x in range(column):
     startX = (x+1)*40
     startY = (y+1)*40
     endX = startX + 40
     endY = startY + 40
     image = cv2.rectangle(image,(startX,startY), (endX,endY), color, thickness) 
 
#=================================================================================
#Qset
environment_rows = row+2
environment_columns = column+2

q_values = np.zeros((environment_rows, environment_columns, 8))

actions = ['up', 'upright', 'right', 'rightdown', 'down', 'downleft', 'left', 'leftup']
#actions = ['up', 'right', 'down', 'left']
#---------------------------------------------------------------------------------

entryG = sys.argv[3]
entryGate = entryG.split(',',2)
xEntry = int(entryGate[0])
yEntry = int(entryGate[1])

exitG = sys.argv[4]
exitGate = exitG.split(',',2)
xExit = int(exitGate[0])
yExit = int(exitGate[1])


#print(environment_columns)
#print(environment_rows)

rewards = np.full((environment_rows, environment_columns), -1.)

#if xEntry==0:
  #xEntry += 1
#  rewards[yEntry+1,1]=-100.
#  if yEntry>1: rewards[yEntry-1,1]=-50.
#elif yEntry==0:
  #yEntry += 1
#  rewards[1,xEntry]=-100.
  #if yEntry>1: rewards[yEntry-1,1]=-100

#if xExit == environment_columns-1:
  #xExit -= 1
#  rewards[yExit-1,xExit-1]=-50.
#  rewards[yExit+1,xExit-1]=-50.
  
  #if yEntry>1: rewards[yEntry-1,1]=-50.
#elif  yExit == environment_rows-1:
#  rewards[yExit-1,xExit]=-50
  #yExit -= 1

#draw border
for x in range(column+1):
     startX = (x+1)*40
     startY = 0
     endX = startX + 40
     endY = startY + 40
     rewards[0,x] = -100.
     points = np.array([[startX, startY], [startX+40, startY], 
                       [startX+40, startY+40], [startX, startY+40]])    
     image = cv2.fillPoly(image, pts=[points], color=(0, 0, 255)) 

for x in range(column+1):
     startX = (x+1)*40
     startY = (row+1)*40
     endX = startX + 40
     endY = startY + 40
     rewards[row+1,x] = -100.
     points = np.array([[startX, startY], [startX+40, startY], 
                       [startX+40, startY+40], [startX, startY+40]])    
     image = cv2.fillPoly(image, pts=[points], color=(0, 0, 255)) 

for y in range(row+2):
     startX = 0
     startY = y*40
     endX = startX + 40
     endY = startY + 40
     rewards[y,0] = -100.
     points = np.array([[startX, startY], [startX+40, startY], 
                       [startX+40, startY+40], [startX, startY+40]])    
     image = cv2.fillPoly(image, pts=[points], color=(0, 0, 255)) 

for y in range(row+2):
     startX = (column+1)*40
     #rewards[column+1, y] = -100.
     startY = y*40
     endX = startX + 40
     endY = startY + 40
     rewards[y, column+1] = -100.
     points = np.array([[startX, startY], [startX+40, startY], 
                       [startX+40, startY+40], [startX, startY+40]])    
     image = cv2.fillPoly(image, pts=[points], color=(0, 0, 255))

rewards[yExit, xExit] = 100. #set the reward for the packaging area (i.e., the goal) to 100
rewards[yEntry, xEntry] = -1. #set the reward for the packaging area (i.e., the goal) to 100

startX = xEntry*40
startY = yEntry*40
endX = startX + 40
endY = startY + 40
points = np.array([[startX, startY], [startX+40, startY], 
                       [startX+40, startY+40], [startX, startY+40]])    
image = cv2.fillPoly(image, pts=[points], color=(0, 255, 255)) 

startX = xExit*40
startY = yExit*40
endX = startX + 40
endY = startY + 40
points = np.array([[startX, startY], [startX+40, startY], 
                       [startX+40, startY+40], [startX, startY+40]])    
image = cv2.fillPoly(image, pts=[points], color=(0, 255, 255)) 

startX = int(entryGate[0])*40
startY = int(entryGate[1])*40
endX = startX + 40
endY = startY + 40
points = np.array([[startX, startY], [startX+40, startY], 
                       [startX+40, startY+40], [startX, startY+40]])    
image = cv2.fillPoly(image, pts=[points], color=(0, 255, 0)) 

startX = int(exitGate[0])*40
startY = int(exitGate[1])*40
endX = startX + 40
endY = startY + 40
points = np.array([[startX, startY], [startX+40, startY], 
                       [startX+40, startY+40], [startX, startY+40]])    
image = cv2.fillPoly(image, pts=[points], color=(255, 0, 0)) 

#define aisle locations (i.e., white squares) for rows 1 through 9
##aisles = {} #store locations in a dictionary
#aisles[1] = [i for i in range(1, 10)]
#aisles[2] = [1, 7, 9]
#aisles[3] = [i for i in range(1, 8)]
#aisles[3].append(9)
#aisles[4] = [3, 7]
#aisles[5] = [i for i in range(11)]
###aisles[6] = [5]
#aisles[7] = [i for i in range(1, 10)]
#aisles[8] = [3, 7]
#aisles[9] = [i for i in range(11)]

#set the rewards for all aisle locations (i.e., white squares)
#for row_index in range(1, 10):
#  for column_index in aisles[row_index]:
#    rewards[row_index, column_index] = -1.
  
#print rewards matrix
for row in rewards:
  print(row)

def is_terminal_state(current_row_index, current_column_index):
  #if the reward for this location is -1, then it is not a terminal state (i.e., it is a 'white square')
  if rewards[current_row_index, current_column_index] == -1.:
    return False
  else:
    return True

#define a function that will choose a random, non-terminal starting location
def get_starting_location():
  #get a random row and column index
  current_row_index = np.random.randint(environment_rows)
  current_column_index = np.random.randint(environment_columns)
  current_action_index = 0
  #continue choosing random row and column indexes until a non-terminal state is identified
  #(i.e., until the chosen state is a 'white square').
  while is_terminal_state(current_row_index, current_column_index):
    current_row_index = np.random.randint(environment_rows)
    current_column_index = np.random.randint(environment_columns)
  return current_row_index, current_column_index

#define an epsilon greedy algorithm that will choose which action to take next (i.e., where to move next)
def get_next_action(current_row_index, current_column_index, epsilon):
  #if a randomly chosen value between 0 and 1 is less than epsilon, 
  #then choose the most promising value from the Q-table for this state.
  if np.random.random() < epsilon:
    return np.argmax(q_values[current_row_index, current_column_index])
  else: #choose a random action
    return np.random.randint(8) #''''''''''iki awale 4

#define a function that will get the next location based on the chosen action
#iki sisan
def get_next_location(current_row_index, current_column_index, action_index):
  new_row_index = current_row_index
  new_column_index = current_column_index
  
  if actions[action_index] == 'up' and current_row_index > 0:
    new_row_index -= 1
  elif actions[action_index] == 'right' and current_column_index < environment_columns - 1:
    new_column_index += 1
  elif actions[action_index] == 'down' and current_row_index < environment_rows - 1:
    new_row_index += 1
  elif actions[action_index] == 'left' and current_column_index > 0:
    new_column_index -= 1
  elif actions[action_index] == 'upright' and current_row_index > 0 and current_column_index < environment_columns - 1:
    new_row_index -= 1
    new_column_index += 1
  elif actions[action_index] == 'rightdown' and current_column_index < environment_columns - 1 and current_row_index < environment_rows - 1:
    new_column_index += 1
    new_row_index += 1
  elif actions[action_index] == 'downleft' and current_row_index < environment_rows - 1 and current_column_index > 0:
    new_row_index += 1
    new_column_index -= 1
  elif actions[action_index] == 'upleft' and current_column_index > 0 and current_row_index > 0:
    new_column_index -= 1
    new_row_index -= 1
  return new_row_index, new_column_index

#Define a function that will get the shortest path between any location within the warehouse that 
#the robot is allowed to travel and the item packaging location.
def get_shortest_path(start_row_index, start_column_index):
  #return immediately if this is an invalid starting location
  if is_terminal_state(start_row_index, start_column_index):
    return []
  else: #if this is a 'legal' starting location
    current_row_index, current_column_index = start_row_index, start_column_index
    shortest_path = []
    arah = []
    shortest_path.append([current_row_index, current_column_index])
    #continue moving along the path until we reach the goal (i.e., the item packaging location)
    while not is_terminal_state(current_row_index, current_column_index):
      #get the best action to take
      #current_action_index = action_index
      action_index = get_next_action(current_row_index, current_column_index, 1.)
      #move to the next location on the path, and add the new location to the list
      current_row_index, current_column_index = get_next_location(current_row_index, current_column_index, action_index)
      shortest_path.append([current_row_index, current_column_index, action_index])
    return shortest_path

epsilon = 0.9 #the percentage of time when we should take the best action (instead of a random action)
discount_factor = 0.9 #discount factor for future rewards
learning_rate = 0.9 #the rate at which the AI agent should learn
nepisode = 1000
textEpsil = "Epsilon: " + str(epsilon)
textDF = "Disc.Fact: " + str(discount_factor)
textLR = "Learn.Rate: " + str(learning_rate)
textEpisode = "Episode:" + str(nepisode)

#run through 1000 training episodes
for episode in range(nepisode):
  #get the starting location for this episode
  row_index, column_index = get_starting_location()

  #continue taking actions (i.e., moving) until we reach a terminal state
  #(i.e., until we reach the item packaging area or crash into an item storage location)
  while not is_terminal_state(row_index, column_index):
    #choose which action to take (i.e., where to move next)
    action_index = get_next_action(row_index, column_index, epsilon)

    #perform the chosen action, and transition to the next state (i.e., move to the next location)
    old_row_index, old_column_index = row_index, column_index #store the old row and column indexes
    row_index, column_index = get_next_location(row_index, column_index, action_index)
    
    #receive the reward for moving to the new state, and calculate the temporal difference
    reward = rewards[row_index, column_index]
    old_q_value = q_values[old_row_index, old_column_index, action_index]
    temporal_difference = reward + (discount_factor * np.max(q_values[row_index, column_index])) - old_q_value

    #update the Q-value for the previous state and action pair
    new_q_value = old_q_value + (learning_rate * temporal_difference)
    q_values[old_row_index, old_column_index, action_index] = new_q_value

print('Training complete!')

get_Q = get_shortest_path(yEntry, xEntry) #starting at row 3, column 9

end_time = time.time()
exec_time = end_time-start_time

print("waktu=", exec_time)
textWaktu = "Time Proc.:"+ "{:.4f}".format(exec_time) + "S"

lenQ = len(get_Q)
print(get_Q)


vx = 2.0
vp = 2.85
vto = 0.0
#print(vto)
last_imact = 0
corner = 0

for y in range(lenQ-2):
      xroute = get_Q[y+1][1]
      yroute = get_Q[y+1][0]     
      imact = get_Q[y+2][2]
      startX = xroute*40
      startY = yroute*40
      endX = startX + 40
      endY = startY + 40
      points = np.array([[startX, startY], [startX+40, startY], 
                       [startX+40, startY+40], [startX, startY+40]])

      if imact == 0 : 
        arrow = iact0
        vto = vto + vp
      elif imact == 1 : 
        arrow = iact1
        vto = vto + vx
      elif imact == 2 : 
        arrow = iact2
        vto = vto + vp
      elif imact == 3 : 
        arrow = iact3
        vto = vto + vx

      elif imact == 4 : 
        arrow = iact4
        vto = vto + vp
      elif imact == 5 : 
        arrow = iact5
        vto = vto + vx
      elif imact == 6 : 
        arrow = iact6
        vto = vto + vp
      elif imact == 7 : 
        arrow = iact7
        vto = vto + vx

      #print("i",imact)
      if imact != last_imact:
        corner += 1 
          
      image[startY:endY,startX:endX] = arrow  
      
      last_imact = imact
      #print("li",last_imact)
      #image = cv2.fillPoly(image, pts=[points], color=(0, 255, 255))

textCorner = "n Corner: " + str(corner)
  
# Displaying the image  
print("kecepatan= ",vto, "V")
print("n corner= ",corner)
textV = "Ts: " + str(lenQ-2) + " / {:.2f}".format(vto) + "V"
#print (textV)
textY = (environment_rows+1)*40
print(textY)

textX = 10
cv2.putText(image, textEpsil, (textX, textY), font, fontScale, (255,0,0), thickness, cv2.LINE_AA)
cv2.putText(image, textLR, (textX, textY+30), font, fontScale, (255,0,0), thickness, cv2.LINE_AA)
cv2.putText(image, textDF, (textX, textY+60), font, fontScale, (255,0,0), thickness, cv2.LINE_AA)
cv2.putText(image, textEpisode, (textX, textY+90), font, fontScale, (255,0,0), thickness, cv2.LINE_AA)

cv2.putText(image, textWaktu, (textX+200, textY), font, fontScale, (255,0,0), thickness, cv2.LINE_AA)
cv2.putText(image, textV, (textX+200, textY+30), font, fontScale, (255,0,0), thickness, cv2.LINE_AA)
cv2.putText(image, textCorner, (textX+200, textY+60), font, fontScale, (255,0,0), thickness, cv2.LINE_AA)
#cv2.putText(image, textEpisode, (textX+100, textY+90), font, fontScale, (255,0,0), thickness, cv2.LINE_AA)


cv2.imshow('Omni Conveyor', image)  

cv2.waitKey(0)