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

  part1(inputArray);
  part2(inputArray);
  console.log(`Done in ${((performance.now() - st) / 1000).toFixed(4)}s`);
}

function part1(input: string[]): void {
  // Generate the map
  map = generateMap(input);

  // Draw the height map
  // draw();

  // Define the starting point
  const startingPoint = map.start!;

  // Set the starting distance to 0
  startingPoint.distance = 0;

  // Traverse the map from this starting point
  const end = traverseMap(startingPoint, 1);

  console.log(`Part1: ${end?.coordinates}: ${end?.distance}`);
  // Print the path we took
  // printPath(startingPoint, end!);
}


function part2(input: string[]): void {
  // Generate the map
  map = generateMap(input);

  // Draw the height map
  // draw();

  // Define the starting point
  const startingPoint = map.end!;

  // Set the starting distance to 0
  startingPoint.distance = 0;

  // Traverse the map from this starting point
  const end = traverseMap(startingPoint, 2);

  console.log(`Part2: ${end?.coordinates}: ${end?.distance}`);
  // Print the path we took
  // printPath(startingPoint, end!);
}
/**
 * Move from this point towards the `end`
 * @param point 
 */
function traverseMap(point: Point, part: number): Point | undefined {

  // Get the neighbors for the given point
  const neighbors = getNeighbors(point, part);

  // Loop through each neighbor
  for (const neighbor of neighbors) {

    if (neighbor.pathVia === undefined || neighbor.distance > point.distance + 1) {
      // Update the neighbor data if it was nto set already or
      // our current path would be faster
      neighbor.pathVia = point;
      neighbor.distance = point.distance + 1;
    }

    if ((part == 1 && neighbor === map.end) || (part == 2 && neighbor.height === 1)) {
      return neighbor;
    }

  };

  // As we already explored all of the neighbors if this point
  // mark it as visited
  visitedPoints.push(point);

  // Sort all the points based on distance not that the current points neighbors were updated
  sortPoints();

  // Run move recursively from the closest point 
  const nextPoint = getNextPoint();
  const result = traverseMap(nextPoint, part);
  // If we found the end return it, or return undefined
  if (result !== undefined) {
    return result;
  }
  return undefined;
}

/**
 * Get the valid neighboring points 
 * @param point - The point we are investigating
 * @param map - The height map
 * @returns - The neighboring points, at a maximum one distance 
 */
function getNeighbors(point: Point, part: number): Point[] {
  const neighbors: Point[] = [];
  [-1, 0, 1].forEach(x => {
    [-1, 0, 1].forEach(y => {
      const coordinates = `${point.x + x}-${point.y + y}`;
      if (!(x === 0 && y === 0) && (x === 0 || y === 0) && coordinates in map.points) {
        // You can move exactly one square up, down, left, or right.
        const neighbor = map.points[coordinates];
        
        // We should not re-visit points
        if (visitedPoints.includes(neighbor)) return;

        if ((part === 1 && neighbor.height - point.height <= 1) || (part === 2 && point.height - neighbor.height <= 1)) {
          // For part1 we want to move to places that are lower or maximum one higher 
          // For part 2 we want move to places that are not lower than one
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

  input.forEach((row, y) => {
    const pointsRow: Point[] = [];
    row.split("").forEach((letter, x) => {
      const coordinates = `${x + 1}-${totalRows - y}`;
      const point: Point = {
        x: x + 1,
        y: totalRows - y,
        coordinates: coordinates,
        height: 0,
        distance: Number.MAX_SAFE_INTEGER,
        pathVia: undefined
      };

      switch (letter) {
        case "S":
          point.height = getHeight("a");
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

function draw(showVisited = false, startX = 1000, startY = 1000, size = 5000): void {

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

/**
 * Print the path that was found between the start and end point
 * @param start - Point where we started
 * @param end - Point where we ended
 */
function printPath(start: Point, end: Point): void {
  console.log(" ");
  const path: string[] = [];
  let point = end;
  while (point !== start) {
    path.unshift(`${point?.coordinates}`);
    point = point.pathVia!;
  }
  console.log(path.join(", "));
}