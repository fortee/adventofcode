import { arraysIntersect, arraysEqual } from "../utils/tools";

/**
 * Main function to trigger all functionality needed to solve the daily challenge
 * @param input - `raw` string content of the input file
 */
export async function solve(input: string, dayNumber: string, usingExample: boolean): Promise<void> {
  console.log(`---- Day ${dayNumber} ----`);

  // Split the string to an array of items
  const inputArray = input.split("");

  // Solve Part 1
  await doit(inputArray, 1, 4);
  // Solve Part 2
  await doit(inputArray, 2, 14);
}

/**
 * @param input - The Puzzle input
 */
async function doit(input: string[], part: number, makerLength: number): Promise<number | void> {

  let index = makerLength;
  const signalLength = input.length;
  while (index <= signalLength) {
    // Loop until the end of the input
    const section = input.slice(index - makerLength, index);

    if (section.length === new Set(section).size) {
      // The section does not contain any duplicate values
      console.log(`Part${part}: ${index}`);
      return index;
    }
    index++;
  }
  console.log(`Part${part}: No 'start-of-packet marker' found!`);

}