import { arraysIntersect, arraysEqual } from "../utils/tools";

/**
 * Main function to trigger all functionality needed to solve the daily challenge
 * @param input - `raw` string content of the input file
 */
export async function solve(input: string, dayNumber: string) {
  console.log(`---- Day ${dayNumber} ----`);

  // Split the string to an array of items
  const inputArray = input.split("\n");

  // Solve Part 1&2
  allParts(inputArray)
}

/**
 * @param input - The Puzzle input
 */
function allParts(input: string[]) {
  let part1 = 0;
  let part2 = 0;
  input.forEach(pair => {
    const sections = pair.split(",").map(x => x.split("-").map(i => +i))

    const result = fullOverLap(sections)

    if (result["fullOverLap"]) {
      part1++;
    }

    if (result["partialOverlap"]) {
      part2++;
    }

  });
  console.log(`Part1: ${part1}`);
  console.log(`Part2: ${part2}`);
}

/**
 * Check if the sections fully overlap each other.
 * This would have been so much easier ion python... :/
 */
function fullOverLap(sections: number[][]): Record<string, boolean> {

  // Generate the array of integers based on the received range
  const left = [...Array(sections[0][1] - sections[0][0] + 1).keys()].map(x => x + sections[0][0]);
  const right = [...Array(sections[1][1] - sections[1][0] + 1).keys()].map(x => x + sections[1][0]);

  // Get the integers that are matching between the two arrays
  const intersect = arraysIntersect(left, right)

  return {
    // If the intersect matches exactly one of the arrays it means one contains the other exactly
    "fullOverLap": arraysEqual(intersect, left) || arraysEqual(intersect, right),
    // If the intersect is not null it means the two arrays have at least one matching item
    "partialOverlap": !arraysEqual(intersect, [])
  }
}