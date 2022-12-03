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
  await part2(inputArray)
}

/**
 * @param input - The Puzzle input
 */
async function part1(input: string[]) {
  let total = 0;
  input.forEach(items => {

    // "...A given rucksack always has the same number of items in each of its two compartments...""
    // Get the left compartment
    const left = items.slice(0, items.length / 2);
    // Get the right compartment
    const right = items.slice(items.length / 2, items.length);

    // Find the common letter between the two compartments
    const [commonLetter] = getCommon(left.split(""), right.split(""))

    // Quantify the common letter
    total += getCharacterPriority(commonLetter);
  });
  console.log(`Part1: ${total}`);
}

/**
 * @param input - The Puzzle input
 */
async function part2(input: string[]) {
  let total = 0;

  while (input.length) {
    // Loop trough the input by groups of 3
    const group = input.splice(0, 3);

    // Get the common letter between the first two bags
    const firstTwoGroupCommonLetters = getCommon(group[0].split(""), group[1].split(""))
    // Get the common letter with the 3rd bag
    const [commonLetter] = getCommon(firstTwoGroupCommonLetters, group[2].split(""))

    // Quantify the common letter
    total += getCharacterPriority(commonLetter);
  }
  console.log(`Part2: ${total}`);
}

/**
 * Get the common item between two arrays
 * @param array1 - First array
 * @param array2 - Second array
 * @returns - The common item between the two arrays
 */
function getCommon(array1: string[], array2: string[]) {
  return array1.filter(x => array2.includes(x));
}

/**
 * Get the priority value of the letter
 * @param letter - The letter we need the priority for
 * @returns The priority of the letter
 */
function getCharacterPriority(letter: string): number {
  const shift = letter.toUpperCase() === letter ? 38 : 96
  return letter.charCodeAt(0) - shift
}
