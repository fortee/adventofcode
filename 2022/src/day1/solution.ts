/**
 * Main function to trigger all functionality needed to solve the daily challenge
 * @param input - `raw` string content of the input file
 */
export async function solve(input: string, dayNumber: string) {
  console.log(`---- Day ${dayNumber} ----`);

  // Split the string to an array of integers based on new lines.
  // Use `null` on empty line (a.k.a new elf)
  const inputArray = input.split("\n").map((x) => (x === "" ? null : +x));

  // Solve Part1&2
  await allParts(inputArray);
}

/**
 * Elf calories
 * @param input - The Puzzle input
 */
async function allParts(input: (number | null)[]) {
  const totals: number[] = [];
  let currentTotal = 0;

  // Loop through all elements
  // add up block for each elf
  // Start new total for each elf
  input.forEach((element) => {
    if (element === null) {
      // `null` represents that a new Elf's block is starting
      totals.push(currentTotal);
      currentTotal = 0;
    } else {
      // Count the calories
      currentTotal += element;
    }
  });

  // Sort the total in descending order
  const totalSorted = totals.sort((a, b) => a - b).reverse();

  // First element is the highest value
  console.log(`Part1: ${totalSorted[0]}`);

  // Splice to the first 3 highest elements than get `sum` with reduce
  console.log(
    `Part2: ${totalSorted.slice(0, 3).reduce((sum, x) => sum + x, 0)}`
  );
}
