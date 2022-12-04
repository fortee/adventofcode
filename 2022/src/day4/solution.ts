import { arrayIntersect } from "../utils/tools";

/**
 * Main function to trigger all functionality needed to solve the daily challenge
 * @param input - `raw` string content of the input file
 */
export async function solve(input: string, dayNumber: string) {
  console.log(`---- Day ${dayNumber} ----`);

  // Split the string to an array of integers based on new lines.
  // Use `null` on empty line (a.k.a new elf)
  const inputArray = input.split("\n");

  // Solve Part 1
  await part1(inputArray)
}

/**
 * @param input - The Puzzle input
 */
async function part1(input: string[]) {
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
  const intersect = arrayIntersect(left, right)

  return {
    // If the intersect matches exactly one of the arrays it means one contains the other exactly
    "fullOverLap": JSON.stringify(intersect) === JSON.stringify(left) || JSON.stringify(intersect) === JSON.stringify(right),
    // If the intersect is not null it means the two arrays have at least one matching item
    "partialOverlap": JSON.stringify(intersect) !== JSON.stringify([])
  }
}