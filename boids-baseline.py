import numpy as np
import matplotlib.pyplot as plt
#Size of canvas. These get updated to fill the whole browser.
width = 150
height = 150

numBoids = 10
visualRange = 75

boids = []

def initBoids():
    i = 0
    while  i < numBoids : 
        boids.append([
            np.random.rand() * width,
            np.random.rand() * height,
            #np.random.rand() * depth,
            np.random.rand() * 10 - 5,
            np.random.rand() * 10 - 5,
            #np.random.rand() * 1 - 0.5,
            []
        ])
        i += 1
    #print(len(boids))

def distance(boid1, boid2):
    return np.sqrt(
        (boid1[0] - boid2[0]) * (boid1[0] - boid2[0]) +
        (boid1[1] - boid2[1]) * (boid1[1] - boid2[1]),
    )


# Constrain a boid to within the window. If it gets too close to an edge,
# nudge it back in and reverse its direction.
def keepWithinBounds(boid): 
    margin = 15
    turnFactor = 1

    if (boid[0] < margin):
        boid[2] += turnFactor
    if (boid[0] > width - margin):
        boid[2] -= turnFactor
    if (boid[1] < margin):
        boid[3] += turnFactor
    if (boid[1] > height - margin):
        boid[3] -= turnFactor

# Find the center of mass of the other boids and adjust velocity slightly to
# point towards the center of mass.
def flyTowardsCenter(boid):
    centeringFactor = 0.005# // adjust velocity by this %

    centerX = 0
    centerY = 0
    numNeighbors = 0

    for otherBoid in boids:
        if distance(boid, otherBoid) < visualRange:
            centerX += otherBoid[0]
            centerY += otherBoid[1]
            numNeighbors += 1

    if (numNeighbors > 0):
        centerX = centerX / numNeighbors
        centerY = centerY / numNeighbors

        boid[2] += (centerX - boid[0]) * centeringFactor
        boid[3] += (centerY - boid[1]) * centeringFactor

#// Move away from other boids that are too close to avoid colliding
def avoidOthers(boid):
    minDistance = 20#; // The distance to stay away from other boids
    avoidFactor = 0.05#; // Adjust velocity by this %
    moveX = 0
    moveY = 0
    for otherBoid in boids:
        dist = distance(boid, otherBoid)
        if (dist < minDistance and dist != 0): 
            moveX += (boid[0] - otherBoid[0]) / dist
            moveY += (boid[1] - otherBoid[1]) / dist

    boid[2] += moveX * avoidFactor
    boid[3] += moveY * avoidFactor

#// Find the average velocity (speed and direction) of the other boids and
#// adjust velocity slightly to match.
def matchVelocity(boid): 
    matchingFactor = 0.05#; // Adjust by this % of average velocity

    avgDX = 0
    avgDY = 0
    numNeighbors = 0

    for otherBoid in boids:
        if (distance(boid, otherBoid) < visualRange):
            avgDX += otherBoid[2]
            avgDY += otherBoid[3]
            numNeighbors += 1

    if (numNeighbors>0):
        avgDX = avgDX / numNeighbors
        avgDY = avgDY / numNeighbors

        boid[2] += (avgDX - boid[2]) * matchingFactor
        boid[3] += (avgDY - boid[3]) * matchingFactor

#// Speed will naturally vary in flocking behavior, but real animals can't go
#// arbitrarily fast.
def limitSpeed(boid):
    speedLimit = 15

    speed = np.sqrt(boid[2] * boid[2] + boid[3] * boid[3])
    if (speed > speedLimit):
        boid[2] = (boid[2] / speed) * speedLimit
        boid[3] = (boid[3] / speed) * speedLimit

#// Main animation loop
exes = []
whys = []
dist = []
to_cohesion = 1001
is_cohesive = False
def main():
  initBoids()
  #// Update each boid
  for i in range(1001):
    totalx = 0
    totaly = 0
    totald = 0
    for boid in boids:
        #// Update the velocities according to each rule
        flyTowardsCenter(boid)
        avoidOthers(boid)
        matchVelocity(boid)
        limitSpeed(boid)
        keepWithinBounds(boid)

        #// Update the position based on the current velocity
        boid[0] += boid[2]
        boid[1] += boid[3]
        boid[4].append([boid[0], boid[1], boid[2], boid[3]])
        #boid[4] = boid[4][-50:]
        totalx += boid[0]
        totaly += boid[1]
        for another_boid in boids:
            totald += distance(boid, another_boid)
    avg = totald / (len(boids) * (len(boids) - 1))
    exes.append(totalx / len(boids))
    whys.append(totaly / len(boids))
    dist.append(avg)
    global is_cohesive, to_cohesion
    if avg < 25 and not is_cohesive:
        to_cohesion = i
        is_cohesive = True




main()
print(to_cohesion)
plt.figure(1)
plt.plot(range(1001), exes)
plt.savefig("exes reference")

plt.figure(2)
plt.plot(range(1001), whys)
plt.savefig("whys reference")

plt.figure(3)
plt.plot(range(1001), dist)
plt.title('Average distance between boids vs Iterations')
plt.xlabel('Iterations')
plt.ylabel("Average distance between boids")
ax3 = plt.gca()
ax3.set_ylim(bottom=0)
plt.savefig("dist reference")