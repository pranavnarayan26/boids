import numpy as np
import matplotlib.pyplot as plt

"""
MILLING WORKS YAY FUCK THIS SHIT IT DOESN'T ANYMORE

width, height = 150
depth = 15
numBoids = 5
visualRange = 75
smellRange = 0
turnFactor = 3
noise = 0
zfactor = width/depth
pheromone = 0.5
minDistance = 10
boid_size = 5
alpha = np.pi/6
radius = np.abs((boid_size + minDistance) / (np.cos(alpha) - np.cos(2 * np.pi / numBoids - alpha)))
mill_radius = radius
if radius >= 1000 or radius <= 1:
    mill_radius = 20
speedLimit = 15


in main():

only do the following:

limitSpeed(boid)
keepWithinBounds(boid)
if i % 5 == 0: 
milling(boid)

and the per boid graph is very useful

"""
iterations = 501
ranges = 1


num = 0
avoidFactor = 0.14
numBoids = 10

smellRange = 75
turnFactor = 3
noise = 0

pheromone = 0.5
minDistance = 10
boid_size = 30
alpha = np.pi / 6
radius = np.abs((boid_size + minDistance) / (np.cos(alpha) - np.cos(2 * np.pi / numBoids - alpha)))
mill_radius = radius
if radius >= 1000 or radius <= 1:
    mill_radius = 20
speedLimit = 15
width = 150
height = 150

depth = width / 10
visualRange = 0
zfactor = width/depth
obstacle_center = (150, 0)
obstacle_radius = 100

exes = []
whys = []
zzzz = []
dist = []
xydist = []
percentages = []
time_together = 0
first_together = iterations

boids = []
isNew = False
obstacleX = np.random.rand() * width
obstacleY = np.random.rand() * height

def initBoids():
    global num
    i = 0
    global boids, exes, whys, zzzz, dist, xydist
    boids = []
    while  i < numBoids : 
        boids.append([
            np.random.rand() * width,
            np.random.rand() * height,
            np.random.rand() * depth, 0, 0, 0,
            #np.random.rand() * 10 - 5,
            #np.random.rand() * 10 - 5,
            #np.random.rand() * 1 - 0.5,
            []
        ])
        i += 1

def distance(boid1, boid2):
    global num
    ret =  np.sqrt(
    (boid1[0] - boid2[0]) * (boid1[0] - boid2[0]) +
      (boid1[1] - boid2[1]) * (boid1[1] - boid2[1]) + (boid1[2] - boid2[2]) * (boid1[2] - boid2[2])
    )
    return ret

def xydistance(boid1, boid2):
    global num
    ret = np.sqrt((boid1[0] - boid2[0]) * (boid1[0] - boid2[0]) + (boid1[1] - boid2[1]) * (boid1[1] - boid2[1]))
    return ret

def angle(boid1, boid2):
    global num
    return np.arctan((boid2[1] - boid1[4])/(boid2[0]-boid1[3]))

def keepWithinBounds(boid):
    global num
    #const margin = 100
    #const turnFactor = 800
    xmargin = width/10 
    ymargin = height/10
    zmargin = depth/10

    if (boid[0] < xmargin):
        boid[3] += turnFactor
    if (boid[0] > width - xmargin):
        boid[3] -= turnFactor
    if (boid[1] < ymargin):
        boid[4] += turnFactor
    if (boid[1] > height - ymargin):
        boid[4] -= turnFactor
    if (boid[2] > depth - zmargin):
        boid[5] -= turnFactor / 10
    if (boid[2] < depth * -1 + zmargin):
        boid[5] += turnFactor / 10
  
    """if (boid[0] < margin) {
        boid[3] += turnFactor / boid[0]
    }
    if (boid[0] > width - margin) {
        boid[3] -= turnFactor / (width - boid[0])
    }
    if (boid[1] < margin) {
        boid[4] += turnFactor / boid[1]
    }
    if (boid[1] > height - margin) {
        boid[4] -= turnFactor / (height - boid[1])
    }"""


def flyTowardsCenter(boid):
    global num
    centeringFactor = 0.005 # adjust velocity by this %

    centerX = 0
    centerY = 0
    centerZ = 0
    numNeighbors = 0

    pX = 0
    pY = 0
    pZ = 0
    numP = 0

    for otherBoid in boids:
        if (visualRange != 0 and distance(boid, otherBoid) < visualRange and visualRange != 0): # interesting note : this also includes the present boid itself
            centerX += otherBoid[0] + np.random.rand() * noise - noise / 2
            centerY += otherBoid[1] + np.random.rand() * noise - noise / 2
            centerZ += otherBoid[2] + np.random.rand() * noise / zfactor - noise / 2 / zfactor
            numNeighbors += 1
        else:
            
            #let distance_weight = 1 / i
            xs = [sublist[0] for sublist in otherBoid[6]]
            ys = [sublist[1] for sublist in otherBoid[6]]
            zs = [sublist[2] for sublist in otherBoid[6]]
            dxs = [sublist[3] for sublist in otherBoid[6]]
            dys = [sublist[4] for sublist in otherBoid[6]]
            dzs = [sublist[5] for sublist in otherBoid[6]]
            i = len(xs)
            for x1, y1, z1, dx1, dy1, dz1 in zip(xs, ys, zs, dxs, dys, dzs):
                hm, _, _ = pointDist(boid, (x1, y1))
                if (smellRange != 0 and (hm < smellRange)):# and np.abs(boid[2] - z1 < smellRange))):
                    pX += (dx1 + np.random.rand() * noise - noise / 2) * i
                    pY += (dy1 + np.random.rand() * noise - noise / 2) * i
                    pY += (dz1 + np.random.rand() * noise / zfactor - noise / 2 / zfactor) * i
                    numP += i
                i -= 1
            

    if (numNeighbors > 0):
        centerX = centerX / numNeighbors
        centerY = centerY / numNeighbors
        centerZ = centerZ / numNeighbors

        boid[3] += (centerX - boid[0]) * centeringFactor
        boid[4] += (centerY - boid[1]) * centeringFactor
        boid[5] += (centerZ - boid[2]) * centeringFactor / 10


    if (numP > 0):
        pX = pX / numP
        pY = pY / numP
        pZ = pZ / numP

        boid[3] += pX * pheromone
        boid[4] += pY * pheromone
        boid[5] += pZ * pheromone / 10


def pointDist(boid, point):
    global num
    x, y = point
    distance = np.sqrt((boid[0] - x)**2 + (boid[1] - y)**2)
    right = boid[0] > x
    above = boid[1] > y
    return distance, right, above
def avoidObstacle(boid):
    global num
    dist, right, above = pointDist(boid, obstacle_center)
    if dist >= obstacle_radius:
        dist -= obstacle_radius
        if dist < 2 * obstacle_radius:
            if right and above:
                boid[3] += avoidFactor/dist
                boid[4] += avoidFactor/dist
            if not right and not above:
                boid[3] -= avoidFactor/dist
                boid[4] -= avoidFactor/dist
            if right and not above:
                boid[3] += avoidFactor/dist
                boid[4] -= avoidFactor/dist
            if not right and above:
                boid[3] -= avoidFactor/dist
                boid[4] += avoidFactor/dist
    else:
        if right and above:
            boid[3] += avoidFactor/(dist/obstacle_radius)
            boid[4] += avoidFactor/(dist/obstacle_radius)
        if not right and not above:
            boid[3] -= avoidFactor/(dist/obstacle_radius)
            boid[4] -= avoidFactor/(dist/obstacle_radius)
        if right and not above:
            boid[3] += avoidFactor/(dist/obstacle_radius)
            boid[4] -= avoidFactor/(dist/obstacle_radius)
        if not right and above:
            boid[3] -= avoidFactor/(dist/obstacle_radius)
            boid[4] += avoidFactor/(dist/obstacle_radius)



def avoidOthers(boid):
    global num
    # The distance to stay away from other boids
    avoidFactor = 0.05 #Adjust velocity by this %
    moveX = 0
    moveY = 0
    moveZ = 0
    for otherBoid in boids: 
        dist = distance(boid, otherBoid)
        if (dist < minDistance and dist != 0):
            moveX += (boid[0] - otherBoid[0]) / dist
            moveY += (boid[1] - otherBoid[1]) / dist
            moveZ += (boid[2] - otherBoid[2]) / dist

    boid[3] += moveX * avoidFactor
    boid[4] += moveY * avoidFactor
    boid[5] += moveZ * avoidFactor / 10

def matchVelocity(boid):
    global num
    matchingFactor = 0.05 #Adjust by this % of average velocity

    avgDX = 0
    avgDY = 0
    avgDZ = 0
    numNeighbors = 0

    for otherBoid in boids:
        if (distance(boid, otherBoid) < visualRange):
            avgDX += otherBoid[3] + np.random.rand() * noise - noise / 2
            avgDY += otherBoid[4] + np.random.rand() * noise - noise / 2
            avgDZ += otherBoid[5] + np.random.rand() * noise / zfactor - noise / 2 / zfactor
            numNeighbors += 1

    if (numNeighbors):
        avgDX = avgDX / numNeighbors
        avgDY = avgDY / numNeighbors
        avgDZ = avgDZ / numNeighbors

        boid[3] += (avgDX - boid[3]) * matchingFactor
        boid[4] += (avgDY - boid[4]) * matchingFactor
        boid[5] += (avgDZ - boid[5]) * matchingFactor / 10

def limitSpeed(boid):
    global num
    speed = np.sqrt(boid[3] * boid[3] + boid[4] * boid[4] + boid[5] * boid[5])
    if (speed > speedLimit):
        boid[3] = (boid[3] / speed) * speedLimit
        boid[4] = (boid[4] / speed) * speedLimit
        boid[5] = (boid[5] / speed) * speedLimit / 10

def wind_influence(): 
    global num
    wind_x = np.random.rand() * 2 - 1
    wind_y = np.random.rand() * 2 - 1
    wind_z = np.random.rand() * 2 - 1

    return [min(0.9 * turnFactor, np.abs(wind_x)), min(0.9 * turnFactor, np.abs(wind_y)), min(0.9 * turnFactor, np.abs(wind_z))]

def turning(left, boid):
    global num
    millFactor = 0.0001
    if (left):
        if (boid[3] >= 0 and boid[4] >= 0):
            boid[3] -= np.pi/180 *mill_radius * millFactor
            boid[4] += np.pi/180 *mill_radius * millFactor
        elif (boid[3] > 0 and boid[4] < 0):
            boid[3] += np.pi/180 *mill_radius * millFactor
            boid[4] += np.pi/180 *mill_radius * millFactor
        elif (boid[3] < 0 and boid[4] > 0):
            boid[3] -= np.pi/180 *mill_radius * millFactor 
            boid[4] -= np.pi/180 *mill_radius * millFactor 
        else:
            boid[3] += np.pi/180 *mill_radius * millFactor 
            boid[4] -= np.pi/180 *mill_radius * millFactor 
    else:
        if (boid[3] >= 0 and boid[4] >= 0):
            boid[3] += np.pi/180 *mill_radius * millFactor 
            boid[4] -= np.pi/180 *mill_radius * millFactor 
        elif (boid[3] > 0 and boid[4] < 0):
            boid[3] -= np.pi/180 *mill_radius * millFactor
            boid[4] -= np.pi/180 *mill_radius * millFactor
        elif (boid[3] < 0 and boid[4] > 0):
            boid[3] += np.pi/180 *mill_radius * millFactor
            boid[4] += np.pi/180 *mill_radius * millFactor
        else:
            boid[3] -= np.pi/180 *mill_radius * millFactor
            boid[4] += np.pi/180 *mill_radius * millFactor

def flyTowardsUnseenCenter(boid):
    boid[3] += (75 - boid[0]) * 0.0025
    boid[4] += (75 - boid[1]) * 0.0025
    boid[5] += (0 - boid[2]) * 0.00025

def stabilize(boid):
    if boid[3] < 0:
        boid[3] += 0.05
    elif boid[3] > 0:
        boid[3] -= 0.05
    if boid[4] < 0:
        boid[4] += 0.05
    elif boid[4] > 0:
        boid[4] -= 0.05
    boid[5] = 0

#milling did not appear to work NVM IT DID YAY
def milling(boid, i):
    global num, alpha, visualRange
    hasSeen = False
    for otherBoid in boids:
        if (otherBoid != boid and np.abs(angle(boid, otherBoid)) <= 2 * alpha and distance(boid, otherBoid) <= visualRange and not hasSeen):
            """if i > iterations / 10:
                flyTowardsCenter(boid)"""
            
            if i % 10 == 0:
                turning(True, boid)
                #matchVelocity(boid)
                avoidOthers(boid)
            
                #stabilize(boid)
            #matchVelocity(boid)
            #avoidOthers(boid)
            hasSeen = True
    if not hasSeen:#if (distance(boid, otherBoid) < visualRange):
        flyTowardsCenter(boid)
        if i % 20 == 0:
            turning(False, boid)
            
        #flyTowardsCenter(boid)
        #matchVelocity(boid)
    
# the problem here appears to be with ctx[0] and cty[1]
"""function obstacle(ctx) {
  ctx.fillStyle = "ffffff";
  let ox = obstacleX;
  let oy = obstacleY;
  ctx.translate(ox, Math.min(oy + 25, height));
  ctx.lineTo(Math.max(ctx[0] - 25, 0), ctx[1]);
  ctx.lineTo(ctx[0], Math.max(ctx[1] - 50, 0));
  ctx.lineTo(Math.min(ctx[0] + 50, width), ctx[1]);
  ctx.lineTo(ctx[0], Math.min(ctx[1] + 50, height));
  
  ctx.fill()
  ctx.setTransform(1, 0, 0, 1, 0, 0);

}"""

wind_strengths = []
avg_wind_dist = []
obstacle_iterations = []
obstacle_dist = []
def main():
    
    initial_together = iterations
    initial = False
    global percentages, exes, whys, zzzz, dist, xydist, wind_strengths, avoidFactor, obstacle_radius, num
    for x in range(ranges):
        timing = 0
        obstacle = 0
        dist = []
        initBoids()
        global speedLimit
        speedLimit = x + 1
        for i in range(iterations):
            num = i
            totalx = 0
            totaly = 0
            totalz = 0
            totald = 0
            totalxy = 0
            wind = [0, 0, 0]
            if i > iterations / 2:
                wind_strengths.append(np.linalg.norm(wind))
            for boid in boids:
                #Update the velocities according to each rule
                flyTowardsCenter(boid)
                #avoidObstacle(boid)
                avoidOthers(boid)
                matchVelocity(boid)
                limitSpeed(boid)
                keepWithinBounds(boid)
                """if i % 10 == 0: 
                    milling(boid, i)"""
                boid[0] += (boid[3]) + wind[0]
                boid[1] += (boid[4]) + wind[1]
                boid[2] += (boid[5]) + wind[2]
                boid[6].append([boid[0], boid[1], boid[2], boid[3], boid[4], boid[5]])
                #boid[6] = boid[6][-iterations:]
                #print(boid[0])
                totalx += boid[0]
                totaly += boid[1]
                totalz += boid[2]
                for another_boid in boids:
                    totald += distance(boid, another_boid)
                    totalxy += xydistance(boid, another_boid)
                obstacle_distance, _, _ = pointDist(boid, obstacle_center)
                if (obstacle_distance <= obstacle_radius):
                    obstacle += 1
            exes.append(totalx / len(boids))
            whys.append(totaly / len(boids))
            zzzz.append(totalz / len(boids))
            dist.append(totald / (len(boids) * (len(boids) - 1)))
            xydist.append(totalxy / (len(boids) * (len(boids) - 1)))
            if (totald / (len(boids) * (len(boids) - 1))) <= (minDistance + 5):
                timing += 1
                if not initial:
                    initial_together = i
                    initial = True
        #obstacle_dist.append(dist[250])
            
        percentages.append(timing / iterations * 100)
        obstacle_iterations.append(obstacle / iterations)
    return timing, initial_together, obstacle_iterations

    

time_together, first_together, obstacle = main()
#obstacle /= len(boids)
#print(f"The avg num of boids within obstacle per iteration was {obstacle}")
print(f"The first iteration with avg distance below min distance is {first_together}/{iterations -1}")

"""plt.figure(-1)
obstacle_dist_range = []
for i in range(ranges):
    obstacle_dist_range.append(i * 5)
plt.plot(obstacle_dist_range, obstacle_dist)
axn = plt.gca()
plt.xlabel('Obstacle Radius')
plt.ylabel('Avg distance between boids')
plt.title('Avg distance between boids vs obstacle radius')
axn.set_xticks(obstacle_dist_range[::4])
axn.set_ylim(bottom=0)
plt.savefig('obstacle distances')

plt.figure(0)
stupid_range = []
for i in range(ranges):
    stupid_range.append(i/100)
plt.plot(stupid_range, obstacle)
plt.title('Number of boids within obstacle region vs avoidFactor')
plt.xlabel('avoidFactor')
plt.ylabel('Avg boids within obstacle region per iteration')
ax0 = plt.gca()
ax0.set_xticks(stupid_range[::2])
plt.savefig("obstacle attempt")


plt.figure(1)
plt.plot(range(iterations * ranges), exes)
plt.savefig("exes")

plt.figure(2)
plt.plot(range(iterations * ranges), whys)
plt.savefig("whys")

plt.figure(3)
plt.plot(range(iterations * ranges), zzzz)
plt.savefig("zzzz")"""

hm = plt.figure(iterations * ranges).add_subplot(projection='3d')
hm.plot(exes, whys, zzzz, label='idk')
hm.legend()
plt.savefig("probably not")

plt.figure(5)
plt.plot(range(iterations * ranges), dist)
plt.title('Average distance between boids vs Iterations')
plt.xlabel('Iterations')
plt.ylabel("Average distance between boids")
ax5 = plt.gca()
ax5.set_ylim(bottom=0)
plt.savefig("average distance over time")

plt.figure(6)
plt.plot(range(iterations * ranges), xydist)
plt.savefig("xydist vs time")

plt.figure(7)
plt.plot(range(1, ranges + 1), percentages)
plt.savefig("percentage within minDistance vs speed limit")

i = 1
trying = plt.figure(8).add_subplot(projection='3d')
#print([sublist[0] for sublist in boids[0][6]])
for boid in boids:
    first_elements = [sublist[0] for sublist in boid[6]]
    second_elements = [sublist[1] for sublist in boid[6]]
    third_elements = [sublist[2] for sublist in boid[6]]
    first_elements = first_elements[::4]
    second_elements = second_elements[::4]
    third_elements = third_elements[::4]
    trying.plot(first_elements, second_elements, third_elements, label = f"boid {i}")
    #trying.set_xlim(0, 150)
    #trying.set_ylim(0, 150)
    trying.set_xlabel('x position')
    trying.set_ylabel('y position')
    trying.set_zlabel('z position')

    trying.set_title('Position per boid - "Pheromones?"')
    i += 1
trying.legend().remove()
plt.savefig("per boid")


"""plt.figure(9)
print(len(wind_strengths))
plt.plot(wind_strengths, dist[(-len(wind_strengths)):])
plt.savefig("avg distance vs wind strength")"""




