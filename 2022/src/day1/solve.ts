import { getInput } from "../utils/input";

export async function solve(dayNumber: string) {
  const input: string = getInput({
    dayNumber: dayNumber,
    example: false,
  });
  console.log(`---- Day ${dayNumber} ----`);

  // Split the string to an array of integers based on new lines
  const inputArray = input.split("\n").map((x) => (x === "" ? null : +x));

  // Solve Part1&2
  await allParts(inputArray);
}

async function allParts(input: (number | null)[]) {
  const totals: number[] = [];
  let currentTotal = 0;
  input.forEach((element) => {
    if (element === null) {
      totals.push(currentTotal);
      currentTotal = 0;
    } else {
      currentTotal += element;
    }
  });

  // Sort the total in descending order
  const totalSorted = totals.sort((a, b) => a - b).reverse();

  // First element is the highest value
  console.log(`Part1: ${totalSorted[0]}`);

  // Splice to the first highest elements than get `sum` with reduce
  console.log(
    `Part2: ${totalSorted.slice(0, 3).reduce((sum, x) => sum + x, 0)}`
  );
}
