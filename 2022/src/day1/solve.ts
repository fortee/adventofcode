import { getInput } from "../utils/input";

export async function solve(dayNumber: string) {
  const input: string = getInput({
    dayNumber: dayNumber,
    example: true,
  });
  console.log(`---- Day ${dayNumber} ----`);

  // Split the string to an array based on new lines
  const inputArray = input.split("\n");

  // Solve Part1
  await part1(inputArray);
}

async function part1(input: string[]) {
  console.log(input);
}
