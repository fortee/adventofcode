import { performance } from 'perf_hooks';

type Point = {
  x: number,
  y: number,
  coordinates: string,
  height: number,
  distance: number,
  pathVia: Point | undefined;
};

type Points = {
  [key: string]: Point;
};

type HeightMap = {
  points: Points,
  orderedPoints: Point[],
  width: number,
  height: number,
  start?: Point,
  end?: Point;
};

let map: HeightMap;

const visitedPoints: Point[] = [];

/**
 * Main function to trigger all functionality needed to solve the daily challenge
 * @param input - `raw` string content of the input file
 */
export async function solve(input: string, dayNumber: string, usingExample: boolean): Promise<void> {
  const st = performance.now();
  console.log(`---- Day ${dayNumber} ----`);

  // Split the string to an array of items
  const inputArray = input.split("\n");

  map = generateMap(inputArray);
  part1();
  console.log(`Done in ${((performance.now() - st) / 1000).toFixed(4)}s`);
}

/**
 * Solve Part 1 of the puzzle
 * @param input - The input as an array of strings
 */
function part1() {
  if (map.start === undefined || map.end === undefined) {
    console.log(`Start or End point not found for map!`);
    return;
  }
  // draw(true);

  // Start to move towards the `end` from the `start`
  const end = move(map.start);
  end === map.end ? console.log(`End found: ${end.coordinates}`) : console.log(`End was not found`);
  console.log("=== PART 1 DONE ===");

}

/**
 * Move from this point towards the `end`
 * @param point 
 */
function move(point: Point): Point | undefined {

  // Get the neighbors for the given point
  const neighbors = getNeighbors(point);

  // Loop through each neighbor
  // console.log(` `);
  // console.log(`${point.coordinates}`);
  for (const neighbor of neighbors) {

    if (neighbor.pathVia === undefined || neighbor.distance > point.distance + 1) {
      // Update the neighbor data if it was nto set already or
      // our current path would be faster
      neighbor.pathVia = point;
      neighbor.distance = point.distance + 1;
      // console.log(`    ${neighbor.coordinates} | ${neighbor.distance} (${neighbor.pathVia.coordinates})`);
    } else {
      // console.log(`    ${neighbor.coordinates} | stays`);
    }

    if (neighbor === map.end) {
      return neighbor;
    }
  };

  // As we already explored all of the neighbors if this point
  // mark it as visited
  visitedPoints.push(point);

  // Sort all the points based on distance not that the current points neighbors were updated
  sortPoints();

  // Run move recursively from the closest point 
  const result = move(getNextPoint());
  // If we found the end return it, or return undefined
  return result !== undefined ? result : undefined;
}

/**
 * Get the valid neighboring points 
 * @param point - The point we are investigating
 * @param map - The height map
 * @returns - The neighboring points, at a maximum one distance 
 */
function getNeighbors(point: Point) {
  const neighbors: Point[] = [];
  [-1, 0, 1].forEach(x => {
    [-1, 0, 1].forEach(y => {
      const coordinates = `${point.x + x}-${point.y + y}`;
      if (!(x === 0 && y === 0) && (x === 0 || y === 0) && coordinates in map.points) {
        // You can move exactly one square up, down, left, or right.
        const neighbor = map.points[coordinates];
        if (neighbor.height - point.height <= 1 && !visitedPoints.includes(neighbor)) {
          // To avoid needing to get out your climbing gear, the elevation of the destination square can be at most one higher
          // than the elevation of your current square; that is, if your current elevation is m, you could step to elevation n,
          // but not to elevation o.
          // (This also means that the elevation of the destination square can be much lower than the elevation of your current square.)
          neighbors.push(neighbor);
        }
      }
    });
  });
  return neighbors;
}

/**
 * Get the height map with numbers instead of integers
 * @param input - Height map with string
 * @returns - Map
 */
function generateMap(input: string[]): HeightMap {
  const map: HeightMap = {
    points: {},
    orderedPoints: [],
    width: input[0].length,
    height: input.length,
  };
  const totalRows = input.length;
  console.log(" ");
  console.log("=== MAP ===");
  console.log(" ");
  input.forEach((row, y) => {
    const pointsRow: Point[] = [];
    row.split("").forEach((letter, x) => {
      const coordinates = `${x + 1}-${totalRows - y}`;
      const point: Point = { x: x + 1, y: totalRows - y, coordinates: coordinates, height: 0, distance: Number.MAX_SAFE_INTEGER, pathVia: undefined };
      switch (letter) {
        case "S":
          point.height = getHeight("a");
          point.distance = 0;
          map.start = point;
          break;
        case "E":
          point.height = getHeight("z");
          map.end = point;
          break;
        default:
          point.height = getHeight(letter);
          break;
      }
      map.points[coordinates] = point;
      map.orderedPoints.push(point);
      pointsRow.push(point);
    });
  });
  console.log(" ");
  return map;
}

/**
 * Get number value of the character representing the height
 * @param letter - The letter we need to convert
 * @returns Number value
 */
function getHeight(letter: string): number {
  return letter.charCodeAt(0) - 96;
}

function draw(showVisited = false, startX = 1000, startY = 1000, size = 5000) {

  console.log(" ");
  console.log("=== PATH ===");
  for (let y = map.height; y >= 1; y--) {
    let row = "";
    for (let x = 1; x <= map.width; x++) {
      const point = map.points[`${x}-${y}`];

      if ((point.x < startX - size / 2 || point.x > startX + size / 2) || (point.y < startY - size / 2 || point.y > startY + size / 2)) {
        // If the point is not in the area we want to see skip it
        continue;
      }

      if (point === map.start) {
        row += pad(`${point.coordinates}[S]`);
        continue;
      }
      if (point === map.end) {
        row += pad(`${point.coordinates}[E]`);
        continue;
      }

      // if (showVisited && visitedPoints.includes(point)) {
      //   row += pad(`-`);
      // } else {
      //   row += pad(`${point.height}`);
      // }
      row += pad(`${point.coordinates}[${point.height}]`);
    }
    // Only print if not empty
    if (row !== "") console.log(row);
  }
}

const pad = (str: string, length = 10, char = ' ') => str.padStart((str.length + length) / 2, char).padEnd(length, char);

/**
 * Get the next point from the priority list that is not yet marked as visited
 * @returns 
 */
function getNextPoint(): Point {
  for (const point of map.orderedPoints) {
    if (!visitedPoints.includes(point)) {
      return point;
    }
  }
  return map.orderedPoints[0];
}
/**
 * Sort the points based on their distance to the start
 */
function sortPoints(): void {
  const sorted = map.orderedPoints.sort((a, b) => a.distance - b.distance);
  map.orderedPoints = sorted;
}