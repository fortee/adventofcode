import { arraysIntersect, arraysEqual } from "../utils/tools";

/**
 * Main function to trigger all functionality needed to solve the daily challenge
 * @param input - `raw` string content of the input file
 */
export async function solve(input: string, dayNumber: string) {
  console.log(`---- Day ${dayNumber} ----`);

  // Split the string to an array of integers based on new lines.
  // Use `null` on empty line (a.k.a new elf)
  const inputArray = input.split("\n");

  const crateMap = getCrateMap(inputArray)

  // Solve Part 1
  await doit(inputArray, crateMap, 1);
  // Solve Part 2
  await doit(inputArray, crateMap, 2);
}

type crateMap = Record<number, (string | null)[]>;

function getCrateMap(input: string[]): crateMap {
  let createsProcessing = true;
  const map: crateMap = {};
  while (createsProcessing) {
    const [row] = input.splice(0, 1)

    // Is this the end of the crate map?
    createsProcessing = !(row === "");

    if (arraysEqual(row.split(" ").filter(x => x !== "").slice(0, 3), ['1', '2', '3']) || row === "") {
      // Don't process the stack label row and the crate map separator row
      continue
    }

    const rowItems = row.split("");

    // Process the crate map input row
    let index = 1;
    while (rowItems.length) {

      // Get the first 4 items,
      // as each item is represented as 3 characters and a white space
      const item = rowItems.splice(0, 4)

      if (!isEmptyItem(item)) {
        // There is a crate ex.: ['[', 'D', ']', ' ']
        addToMap(map, index, item[1])
      }
      index++;
    }
  }
  return map;
};

/**
 * Check if the item is empty
 * @param item - Array of strings
 * @returns boolean
 */
function isEmptyItem(item: string[]): boolean {
  for (const x of item) {
    if (x !== " ") {
      return false
    }
  }
  return true

}

/**
 * Add an element to the map to the correct index
 */
function addToMap(map: crateMap, index: number, item: string | null): void {
  // Find the existing stack based on the given index
  const stack = map[index] === undefined ? [] : map[index]
  // Add the item to the bottom of the stack
  // We do this as we are reading the stack top to bottom 
  stack.unshift(item);
  map[index] = stack;
}

/**
 * @param input - The Puzzle input
 */
async function doit(input: string[], crateMap: crateMap, part: number) {
  // Deep copy the map as we will don't want to alter the original
  const map: crateMap = JSON.parse(JSON.stringify(crateMap));
  for (const instructionRow of input) {
    // Process the instructions
    const instructions = instructionRow.split(" ")
    const amount = +instructions[1];
    const src = +instructions[3];
    const dst = +instructions[5];

    // Get the crates we need to move in one go
    const sourceStack = map[src];
    const cratesToMove = sourceStack.splice(sourceStack.length - amount, sourceStack.length)
    if (part === 1) {
      cratesToMove.reverse()
    }

    // Add the crates to the destination
    const destinationStack = map[dst];
    map[dst] = destinationStack.concat(cratesToMove);
  }
  let code = '';
  for (const [i, stack] of Object.entries(map)) {
    code = `${code}${stack.slice(-1)}`
  }
  console.log(`Part${part}: ${code}`);
}