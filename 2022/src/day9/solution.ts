import { performance } from 'perf_hooks';

type Position = {
  x: number,
  y: number;
};


const positions: Record<number, Position> = {};

const numberOfKnots = 10; // The first knot is the Head!

const visitedPositions: Record<number, Position[]> = {};

// Generate the starting data
for (let i = 0; i < numberOfKnots; i++) {
  positions[i] = { x: 0, y: 0 };
  visitedPositions[i] = [{ x: 0, y: 0 }];
}

/**
 * Main function to trigger all functionality needed to solve the daily challenge
 * @param input - `raw` string content of the input file
 */
export async function solve(input: string, dayNumber: string, usingExample: boolean) {
  const st = performance.now();
  console.log(`---- Day ${dayNumber} ----`);

  // Split the string to an array of items
  const inputArray = input.split("\n");

  if (usingExample) {
    console.log("");
    console.log("== Initial State ==");
    console.log("");
    draw();
  }

  for (const line of inputArray) {
    if (usingExample) {
      console.log("");
      console.log(`== ${line} ==`);
      console.log("");
    }

    const [direction, move] = line.split(" ");
    for (let i = 0; i < +move; i++) {
      moveKnots(direction);
    }
    if (usingExample) draw();
  }

  if (usingExample) {
    console.log("");
    console.log("== VISITED ==");
    console.log("");
    draw(true);
  }
  console.log(`Part1: ${visitedPositions[1].length}`);
  console.log(`Part2: ${visitedPositions[9].length}`);
  console.log(`Done in ${((performance.now() - st) / 1000).toFixed(4)}s`);
}

/**
 * Small wrapper function to handle Knot movements
 * @param direction 
 */
function moveKnots(direction: string) {
  for (const knotId in positions) {
    if (+knotId === 0) {
      // The first knot is the Head!
      moveHead(direction, +knotId);
    } else {
      moveKnot(+knotId);
    }

  }
}

/**
 * Move the Head in the given direction and amount
 * @param direction - The direction the head should moves to. U/D changes y, R/L changes x
 * @param move - The amount of the change
 */
function moveHead(direction: string, knotId: number) {

  // The first knot is the Head!
  const knot = positions[knotId];
  // Move the Head
  switch (direction) {
    case 'U':
      knot.y += 1;
      break;
    case 'D':
      knot.y -= 1;
      break;
    case 'R':
      knot.x += 1;
      break;
    case 'L':
      knot.x -= 1;
      break;
    default:
      break;
  }
  // Keep track of positions each know visited
  addToVisitedPositions(knotId, knot);
}

/**
 * Move the Knot so it follows the knot in front of it
 */
function moveKnot(knotId: number) {

  // Get the knot we need to move
  const knot = positions[knotId];

  // Find the reference knot our current knot must follow
  // each knot follows the previous one
  let referenceKnot = positions[knotId - 1];

  if (Math.abs(referenceKnot.x - knot.x) > 1 || Math.abs(referenceKnot.y - knot.y) > 1) {
    // Move the Knot
    if (knot.x == referenceKnot.x) {
      // They are in the same column
      referenceKnot.y - knot.y > 0 ? knot.y = referenceKnot.y - 1 : knot.y = referenceKnot.y + 1;
    } else if (knot.y == referenceKnot.y) {
      // They are in the same row
      referenceKnot.x - knot.x > 0 ? knot.x = referenceKnot.x - 1 : knot.x = referenceKnot.x + 1;
    } else {
      // They are on a different row and column, move diagonally
      referenceKnot.y - knot.y > 0 ? knot.y += 1 : knot.y -= 1;
      referenceKnot.x - knot.x > 0 ? knot.x += 1 : knot.x -= 1;
    }
    // Keep track of positions each know visited
    addToVisitedPositions(knotId, knot);
  }
}

/**
 * Add a given position to the unique list of already visited positions
 */
function addToVisitedPositions(knotId: number, position: Position): void {
  if (!isVisitedPosition(knotId, position)) {
    visitedPositions[knotId].push({ ...position });
  }
}

/**
* Check if the given x,y position is in the visited positions 
* @param knotId - Id of the knot
* @param x - X position
* @param y - Y position
* @returns - Returns if the given x,y position is in the visited positions 
*/
function isVisitedPosition(knotId: number, position: Position): boolean {
  for (const visitedPosition of visitedPositions[knotId]) {
    if (visitedPosition.x == position.x && visitedPosition.y == position.y) {
      return true;
    }
  }
  return false;
}

/**
 * Plot the positions of the knots and visited points
 */
function draw(visited = false): void {

  const size = 50;
  for (let y = size / 2; y >= -(size / 2); y--) {
    let row = '';
    for (let x = -(size / 2); x <= size / 2; x++) {
      if (visited) {
        if (x == 0 && y == 0) {
          row += 's';
        } else if (isVisitedPosition(9, { x: x, y: y })) {
          // The Knot for which we plot the visited positions is hard coded!
          // For Part:1 it should be 1, for Part2: 9
          row += '#';
        } else {
          row += '.';
        }
      } else {

        let hasKnot = false;
        for (const [knotId, knotPosition] of Object.entries(positions)) {
          if (hasKnot) continue;
          if (knotPosition.x == x && knotPosition.y == y) {
            const sign = +knotId === 0 ? 'H' : +knotId;
            row += sign;
            hasKnot = true;
          }
        }
        if (!hasKnot) row += '.';
      }
    }
    console.log(row);
  }
  console.log("");

}