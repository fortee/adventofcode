import { performance } from 'perf_hooks';

type Point = {
  x: number,
  y: number,
  coordinates: string,
  height: number;
};

type Points = {
  [key: string]: Point;
};

type HeightMap = {
  points: Points;
  start?: Point,
  end?: Point,
};

let map: HeightMap;

/**
 * Main function to trigger all functionality needed to solve the daily challenge
 * @param input - `raw` string content of the input file
 */
export async function solve(input: string, dayNumber: string, usingExample: boolean): Promise<void> {
  const st = performance.now();
  console.log(`---- Day ${dayNumber} ----`);

  // Split the string to an array of items
  const inputArray = input.split("\n");
  map = getMap(inputArray);
  part1();
  console.log(`Part1: ${1}`);
  console.log(`Part2: ${2}`);
  console.log(`Done in ${((performance.now() - st) / 1000).toFixed(4)}s`);
}

/**
 * Solve Part 1 of the puzzle
 * @param input - The input as an array of strings
 */
function part1() {
  if (map.start === undefined || map.end === undefined) {
    console.log(`Start or End point found for map!`);
    return;
  }
  // Start to move towards the `end` from the `start`
  moveToEnd(map.start);
}

/**
 * Move from this point towards the `end`
 * @param point 
 */
function moveToEnd(point: Point) {
  const neighbors = getPossibleMoves(point);
  neighbors.forEach(neighbor => {
    if (neighbor === map.end) {
      console.log(`Found end!`);
      return;
    }
    console.log(`${point.coordinates} -> ${neighbor.coordinates}`);
    
    return moveToEnd(neighbor);
  });
}

/**
 * Get the neighbors that are at most one higher, or lower in height
 * @param point - The point we want to move from
 * @param map - The height map
 * @returns - List of valid point we can move to
 */
function getPossibleMoves(point: Point) {
  return getNeighbors(point).filter(p => p.height - point.height <= 1);
}

/**
 * Get the neighboring points 
 * @param point - The point we are investigating
 * @param map - The height map
 * @returns - The neighboring points, at a maximum one distance 
 */
function getNeighbors(point: Point) {
  const neighbors: Point[] = [];
  [-1, 0, 1].forEach(x => {
    [-1, 0, 1].forEach(y => {
      const coordinates = `${point.x + x}-${point.y + y}`;
      if (!(x === 0 && y === 0) && coordinates in map) {
        neighbors.push(map.points[coordinates]);
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
function getMap(input: string[]): HeightMap {
  const map: HeightMap = {
    points: {}
  };
  const totalRows = input.length;
  console.log(" ");
  console.log("=== MAP ===");
  console.log(" ");
  input.forEach((row, y) => {
    let numRow = "";
    row.split("").forEach((letter, x) => {
      const coordinates = `${x + 1}-${totalRows - y}`;
      const point: Point = { x: x + 1, y: totalRows - y, coordinates: coordinates, height: 0 };
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
      numRow += `[${coordinates} (${point.height} )]`;
    });
    console.log(numRow);
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