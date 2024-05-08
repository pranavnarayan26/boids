/* Ideas: use the array "history" to try to implement a sort of pheromone-like system to guide movement: if a boid crosses another's trail, it turns
towards it, and it would realize that it's crossed another's trail by checking the last few entries of "history" (say, the last 10) and turning by
a factor of how close to the end of "history" the point it crossed is.  DONE

implement the milling algorithm from that paper. FAILED

add noise DONE?

add lighting differences and sensitivity things

3D effect by changing boid size SOMEWHAT DONE?

collect data on things like cohesion and time to cohesion and shit like that

have a tracer to find the "center of mass" of all the boids as the simulation runs

read some papers and implement the things they did with boids
*/ 

/* things changed:
turning factor was initially 1
  on a related note, it also didn't scale turningfactor by x and y - which may or may not work, anyway - and it wasn't a global variable
history initially did not store velocities
the entire pheromone thing in flyTowardsCenter
visualRange was initially 75
turned off matchVelocity
wind influence
the obstacle - though that doesn't seem to work
*/



// Size of canvas. These get updated to fill the whole browser.
let width = 150;
let height = 150;

let depth = 30;

let avoidFactor = 0.15;
let obstacle_center = [0, 0];
let obstacle_radius = 1000;


let numBoids = 50;
let visualRange = 0;
let smellRange = 75;
let turnFactor = 3;
let noise = 0;
let zfactor = width/depth;
let pheromone = 0.5;
let minDistance = 20;
let boid_size = 30;
let alpha = Math.PI / 6;
let mill_radius = boid_size / (Math.cos(alpha) - Math.cos(2 * Math.PI / numBoids - alpha)) 
let speedLimit = 15;

var boids = [];
var isNew = false;

function initBoids() {
  for (var i = 0; i < numBoids; i += 1) {
    boids[boids.length] = {
      x: Math.random() * width,
      y: Math.random() * height,
      z: Math.random() * depth,
      dx: Math.random() * 10 - 5,
      dy: Math.random() * 10 - 5,
      dz: Math.random() * 1 - 0.5,
      history: [],
    };
  }
}

function distance(boid1, boid2) {
  return Math.sqrt(
    (boid1.x - boid2.x) * (boid1.x - boid2.x) +
      (boid1.y - boid2.y) * (boid1.y - boid2.y), + (boid1.z - boid2.z)
  );
}

function angle(boid1, boid2) {
  if (boid2.x - boid1.x == 0) {
    return 0;
  }
  else {
    return Math.atan((boid2.y - boid1.y)/(boid2.x-boid1.x));
  }
}

// TODO: This is naive and inefficient.
function nClosestBoids(boid, n) {
  // Make a copy
  const sorted = boids.slice();
  // Sort the copy by distance from `boid`
  sorted.sort((a, b) => distance(boid, a) - distance(boid, b));
  // Return the `n` closest
  return sorted.slice(1, n + 1);
}

// Called initially and whenever the window resizes to update the canvas
// size and width/height variables.
function sizeCanvas() {
  canvas = document.getElementById("boids");
  width = window.innerWidth;
  height = window.innerHeight;
  canvas.width = width;
  canvas.height = height;
}
/*function sizeCanvas() {
  const canvas = document.getElementById("boids");
  const container = canvas.parentElement; // Assuming the canvas is contained within a parent element

  // Calculate the aspect ratio of the canvas
  const canvasAspectRatio = canvas.width / canvas.height;

  // Get the dimensions of the container
  const containerWidth = container.clientWidth;
  const containerHeight = container.clientHeight;

  // Calculate the new dimensions for the canvas while maintaining its aspect ratio
  let newWidth, newHeight;
  if (containerWidth / containerHeight > canvasAspectRatio) {
    // Container is wider than the canvas, so use the container's height as the reference
    newWidth = containerHeight * canvasAspectRatio;
    newHeight = containerHeight;
  } else {
    // Container is taller than the canvas, so use the container's width as the reference
    newWidth = containerWidth;
    newHeight = containerWidth / canvasAspectRatio;
  }

  // Set the new dimensions for the canvas
  canvas.width = newWidth;
  canvas.height = newHeight;
}*/


// Constrain a boid to within the window. If it gets too close to an edge,
// nudge it back in and reverse its direction.
function keepWithinBounds(boid) {
  //const margin = 100;
  //const turnFactor = 800;
  const xmargin = width/10, ymargin = height/10, zmargin = depth/10;

  if (boid.x < xmargin) {
    boid.dx += turnFactor;
  }
  if (boid.x > width - xmargin) {
    boid.dx -= turnFactor;
  }
  if (boid.y < ymargin) {
    boid.dy += turnFactor;
  }
  if (boid.y > height - ymargin) {
    boid.dy -= turnFactor;
  }
  if (boid.z > depth - zmargin) {
    boid.dz -= turnFactor / 10;
  }
  if (boid.z < depth * -1 + zmargin) {
    boid.dz += turnFactor / 10;
  }
  /*if (boid.x < margin) {
    boid.dx += turnFactor / boid.x;
  }
  if (boid.x > width - margin) {
    boid.dx -= turnFactor / (width - boid.x);
  }
  if (boid.y < margin) {
    boid.dy += turnFactor / boid.y;
  }
  if (boid.y > height - margin) {
    boid.dy -= turnFactor / (height - boid.y);
  }*/
}

// Find the center of mass of the other boids and adjust velocity slightly to
// point towards the center of mass.
function flyTowardsCenter(boid) {
  const centeringFactor = 0.005; // adjust velocity by this %

  let centerX = 0;
  let centerY = 0;
  let centerZ = 0;
  let numNeighbors = 0;

  let pX = 0, pY = 0, pZ = 0, numP = 0;

  for (let otherBoid of boids) {
    if (distance(boid, otherBoid) < visualRange && visualRange != 0) { // interesting note : this also includes the present boid itself
      centerX += otherBoid.x + Math.random() * noise - noise / 2;
      centerY += otherBoid.y + Math.random() * noise - noise / 2;
      centerZ += otherBoid.z + Math.random() * noise / zfactor - noise / 2 / zfactor;
      numNeighbors += 1;
    }
    else {
      let i = otherBoid.history.length;  
      //let distance_weight = 1 / i
      for (let location of otherBoid.history) {
        if (Math.abs(boid.x - location[0]) < smellRange && Math.abs(boid.y - location[1]) < smellRange && smellRange != 0) {
          pX += (location[3] + Math.random() * noise - noise / 2) * i;
          pY += (location[4] + Math.random() * noise - noise / 2) * i;
          pY += (location[5] + Math.random() * noise / zfactor - noise / 2 / zfactor) * i;
          numP += i;
        }
        i -= 1;
      }
    } 
  }

  if (numNeighbors) {
    centerX = centerX / numNeighbors;
    centerY = centerY / numNeighbors;
    centerZ = centerZ / numNeighbors;

    boid.dx += (centerX - boid.x) * centeringFactor;
    boid.dy += (centerY - boid.y) * centeringFactor;
    boid.dz += (centerZ - boid.z) * centeringFactor / 10;
  }


  if (numP) {
    pX = pX / numP;
    pY = pY / numP;
    pZ = pZ / numP;

    boid.dx += pX * pheromone;
    boid.dy += pY * pheromone;
    boid.dz += pZ * pheromone / 10;
  }

  
}

// Move away from other boids that are too close to avoid colliding
function avoidOthers(boid) {
 // The distance to stay away from other boids
  const avoidFactor = 0.05; // Adjust velocity by this %
  let moveX = 0;
  let moveY = 0;
  let moveZ = 0;
  for (let otherBoid of boids) {
    if (otherBoid !== boid) {
      if (distance(boid, otherBoid) < minDistance) {
        moveX += boid.x - otherBoid.x;
        moveY += boid.y - otherBoid.y;
        moveZ += (boid.z - otherBoid.z) / zfactor;
      }
    }
  }

  boid.dx += moveX * avoidFactor;
  boid.dy += moveY * avoidFactor;
  boid.dz += moveZ * avoidFactor / 10;
}

// Find the average velocity (speed and direction) of the other boids and
// adjust velocity slightly to match.
function matchVelocity(boid) {
  const matchingFactor = 0.05; // Adjust by this % of average velocity

  let avgDX = 0;
  let avgDY = 0;
  let avgDZ = 0;
  let numNeighbors = 0;

  for (let otherBoid of boids) {
    if (distance(boid, otherBoid) < visualRange) {
      avgDX += otherBoid.dx + Math.random() * noise - noise / 2;
      avgDY += otherBoid.dy + Math.random() * noise - noise / 2;
      avgDZ += otherBoid.dz + Math.random() * noise / zfactor - noise / 2 / zfactor;
      numNeighbors += 1;
    }
  }

  if (numNeighbors) {
    avgDX = avgDX / numNeighbors;
    avgDY = avgDY / numNeighbors;
    avgDZ = avgDZ / numNeighbors;

    boid.dx += (avgDX - boid.dx) * matchingFactor;
    boid.dy += (avgDY - boid.dy) * matchingFactor;
    boid.dz += (avgDZ - boid.dz) * matchingFactor / 10;
  }
}

// Speed will naturally vary in flocking behavior, but real animals can't go
// arbitrarily fast.
function limitSpeed(boid) {

  const speed = Math.sqrt(boid.dx * boid.dx + boid.dy * boid.dy + boid.dz * boid.dz);
  if (speed > speedLimit) {
    boid.dx = (boid.dx / speed) * speedLimit;
    boid.dy = (boid.dy / speed) * speedLimit;
    boid.dz = (boid.dz / speed) * speedLimit / 10;
  }
}

function pointDist(boid, point) {
    [x, y] = point;
    smth = Math.sqrt(Math.pow(boid.x - x, 2) + Math.pow(boid.y - y, 2));
    right = boid.x > x;
    above = boid.y > y;
    return [smth, right, above];
}
function avoidObstacle(boid) {
    [dist, right, above] = pointDist(boid, obstacle_center);
    if (dist >= obstacle_radius){
        dist -= obstacle_radius;
        if (dist < 2 * obstacle_radius && dist !== 0) {  
            if (right && above) {
                boid.dx += avoidFactor/dist;
                boid.dy += avoidFactor/dist;
            }
            if (!right && !above){
                boid.dx -= avoidFactor/dist;
                boid.dy -= avoidFactor/dist;
            }
            if (right && !above) {
                boid.dx += avoidFactor/dist;
                boid.dy -= avoidFactor/dist;
            }
            if (!right && above) {
                boid.dx -= avoidFactor/dist;
                boid.dy += avoidFactor/dist;
            }
        }
    } else if (dist !== 0) {
        if (right && above) {
            boid.dx += avoidFactor/(dist/obstacle_radius);
            boid.dy += avoidFactor/(dist/obstacle_radius);
        }
        if (!right && !above) {
            boid.dx -= avoidFactor/(dist/obstacle_radius);
            boid.dy -= avoidFactor/(dist/obstacle_radius);
        }
        if (right && !above) {
            boid.dx += avoidFactor/(dist/obstacle_radius);
            boid.dy -= avoidFactor/(dist/obstacle_radius);
        }
        if (!right && above) {
            boid.dx -= avoidFactor/(dist/obstacle_radius);
            boid.dy += avoidFactor/(dist/obstacle_radius);
        }
    }
}

const DRAW_TRAIL = true;

function drawBoid(ctx, boid) {
  const angle = Math.atan2(boid.dy, boid.dx);
  horiz = (boid.z + boid_size);
  vert = (boid.z + boid_size) / 3;
  ctx.moveTo(0, 0);
  ctx.translate(boid.x, boid.y);
  ctx.rotate(angle);
  ctx.translate(-boid.x, -boid.y);
  ctx.fillStyle = "#558cf4";
  ctx.beginPath();
  ctx.moveTo(boid.x, boid.y);
  ctx.lineTo(boid.x - horiz, boid.y + vert); //this line and the next seem to control size
  ctx.lineTo(boid.x - horiz, boid.y - vert);
  ctx.lineTo(boid.x, boid.y);
  ctx.fill();
  ctx.setTransform(1, 0, 0, 1, 0, 0);

  if (DRAW_TRAIL) {
    ctx.strokeStyle = "#558cf466";
    ctx.beginPath();
    ctx.moveTo(boid.history[0][0], boid.history[0][1]);
    for (const point of boid.history) {
      ctx.lineTo(point[0], point[1]);
    }
    ctx.stroke();
  }/*
  ctx.strokeStyle = "#558cf466";
  ctx.beginPath();
  ctx.moveTo(0, 0);
  ctx.lineTo(obstacle_center[0], obstacle_center[1]);
  ctx.stroke();*/

}

function wind_influence() {
  let wind_x = 0, wind_y = 0, wind_z = 0;

  return {x: Math.min(0.9 * turnFactor, wind_x), y: Math.min(0.9 * turnFactor, wind_y), z: Math.min(0.9 * turnFactor, wind_z)}

}

function turning(left, boid) {
  if (left) {
    if (boid.dx >= 0 && boid.dy >= 0) {
      boid.dx -= Math.tan(Math.PI/180) *mill_radius / speedLimit;
      boid.dy += Math.tan(Math.PI/180) *mill_radius / speedLimit;
    }
    else if (boid.dx > 0 && boid.dy < 0) {
      boid.dx += Math.tan(Math.PI/180) *mill_radius / speedLimit;
      boid.dy += Math.tan(Math.PI/180) *mill_radius / speedLimit;
    }
    else if (boid.dx < 0 && boid.dy > 0) {
      boid.dx -= Math.tan(Math.PI/180) *mill_radius / speedLimit;
      boid.dy -= Math.tan(Math.PI/180) *mill_radius / speedLimit;
    }
    else {
      boid.dx += Math.tan(Math.PI/180) *mill_radius / speedLimit;
      boid.dy -= Math.tan(Math.PI/180) *mill_radius / speedLimit;
    }
  } else {
    if (boid.dx >= 0 && boid.dy >= 0) {
      boid.dx += Math.tan(Math.PI/180) *mill_radius / speedLimit;
      boid.dy -= Math.tan(Math.PI/180) *mill_radius / speedLimit;
    }
    else if (boid.dx > 0 && boid.dy < 0) {
      boid.dx -= Math.tan(Math.PI/180) *mill_radius / speedLimit;
      boid.dy -= Math.tan(Math.PI/180) *mill_radius / speedLimit;
    }
    else if (boid.dx < 0 && boid.dy > 0) {
      boid.dx += Math.tan(Math.PI/180) *mill_radius / speedLimit;
      boid.dy += Math.tan(Math.PI/180) *mill_radius / speedLimit;
    }
    else {
      boid.dx -= Math.tan(Math.PI/180) *mill_radius / speedLimit;
      boid.dy += Math.tan(Math.PI/180) *mill_radius / speedLimit;
    }
  }
}

//milling did not appear to work
function milling(boid) {
  

  for (let otherBoid of boids) {
    if (Math.abs(angle(boid, otherBoid)) <= alpha && distance(boid, otherBoid) < visualRange) {
      turning(true, boid)
    }
    else if (distance(boid, otherBoid) < visualRange) {
      turning(false, boid)
    }
  }


}
// the problem here appears to be with ctx.x and cty.y
/*function obstacle(ctx) {
  ctx.fillStyle = "ffffff";
  let ox = obstacleX;
  let oy = obstacleY;
  ctx.translate(ox, Math.min(oy + 25, height));
  ctx.lineTo(Math.max(ctx.x - 25, 0), ctx.y);
  ctx.lineTo(ctx.x, Math.max(ctx.y - 50, 0));
  ctx.lineTo(Math.min(ctx.x + 50, width), ctx.y);
  ctx.lineTo(ctx.x, Math.min(ctx.y + 50, height));
  
  ctx.fill()
  ctx.setTransform(1, 0, 0, 1, 0, 0);

}*/

// Main animation loop
function animationLoop() {
  // Update each boid
  for (let boid of boids) {
    // Update the velocities according to each rule
    flyTowardsCenter(boid);
    //avoidObstacle(boid)
    avoidOthers(boid);
    matchVelocity(boid);
    limitSpeed(boid);
    keepWithinBounds(boid);
    //milling(boid)
    // Update the position based on the current velocity
    boid.x += (boid.dx);// + wind_influence().x);
    boid.y += (boid.dy);// + wind_influence().y);
    boid.z += (boid.dz);// + wind_influence().z);
    //boid.z = 0
    boid.history.push([boid.x, boid.y, boid.z, boid.dx, boid.dy, boid.dz])
    boid.history = boid.history.slice(-100);
  }

  // Clear the canvas and redraw all the boids in their current positions
  const ctx = document.getElementById("boids").getContext("2d");
  ctx.clearRect(0, 0, width, height);
  //obstacle(ctx);
  for (let boid of boids) {
    drawBoid(ctx, boid);
  }
  // Schedule the next frame
  window.requestAnimationFrame(animationLoop);
}

window.onload = () => {
  // Make sure the canvas always fills the whole window
  window.addEventListener("resize", sizeCanvas, false);
  sizeCanvas();

  // Randomly distribute the boids to start
  initBoids();

  
  
  // Schedule the main animation loop
  window.requestAnimationFrame(animationLoop);
};

function updateSmell(val) {
  smellRange = val;
}

function updateNoise(val) {
  noise = val;
}

function updateP(val) {
  pheromone = val;
}

function updateSize(val) {
  boid_size = val;
}
/*var slider = document.getElementById("noise");
 // Display the default slider value

// Update the current slider value (each time you drag the slider handle)
slider.oninput = function() {
  smellRange = this.value;
}*/
