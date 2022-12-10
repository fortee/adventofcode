import { performance } from 'perf_hooks';

// Set defaults for variables
let cycleCounter = 0;
let pixelPosition = 0;
let register = 1;
let screenRow: string = "";
const screen: string[] = [];
const signalStrengths: number[] = [];
const getPixel = (): string => { return [register - 1, register, register + 1].includes(pixelPosition) ? '#' : '.'; };

/**
 * Main function to trigger all functionality needed to solve the daily challenge
 * @param input - `raw` string content of the input file
 */
export async function solve(input: string, dayNumber: string, usingExample: boolean): Promise<void> {
  const st = performance.now();
  console.log(`---- Day ${dayNumber} ----`);

  // Split the string to an array of items
  const inputArray = input.split("\n");

  // Loop through each line
  for (const instruction of inputArray) {
    // Split to get the command and value
    const [command, value] = instruction.split(" ");
    // Each instruction takes at least one cycle
    cycle();

    if (command === 'addx') {
      // Adding to the register takes another cycle
      // first we cycle
      cycle();
      // than update the register
      register += +value;
    }
  }
  // Part 1
  console.log(`Part1: ${signalStrengths.reduce(function (product, value) { return product + value; })}`);
  // Part 2
  console.log(`Part2: `);
  display();
  console.log(`Done in ${((performance.now() - st) / 1000).toFixed(4)}s`);
}

/**
 * The cycle
 * @param instruction 
 */
function cycle(): void {

  // Up-count the cycle
  cycleCounter++;

  // Check if we should store the signal strength
  if (cycleCounter === 20 || cycleCounter % 40 === 20) {
    signalStrengths.push(cycleCounter * register);
  }

  // Add the pixel
  addPixelToScreen();

}

/**
 * Add the current pixel to the screen
 */
function addPixelToScreen(): void {
  screenRow += getPixel();
  if (screenRow.length >= 40) {
    screen.push(screenRow);
    pixelPosition = 0;
    screenRow = "";
  } else {
    pixelPosition++;
  }
}

/**
 * Draw the screen
 */
function display(): void {
  console.log("");
  screen.map(row => console.log(row));
  console.log("");
}