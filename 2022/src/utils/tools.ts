import { join } from "path";
import { readFileSync } from "fs";

/**
 * The options we accept for the getInput() method
 */
type getInputOptions = {
  // Represent the number of the day this solution is for
  dayNumber: string;
  //  Should we use the real or example input
  example: boolean;
};

/**
 * Read in the input file for the given day
 * @param options - The options that define which input file to read
 * @returns - `raw` content of the inout file
 */
export function getInput(options: getInputOptions): string {
  const file = options.example ? "input_example" : "input";
  return readFileSync(
    join(__dirname, `../../src/day${options.dayNumber}/${file}`),
    "utf-8"
  );
}

/**
 * Get the common item between two arrays
 * @param array1 - First array
 * @param array2 - Second array
 * @returns - The common items between the two arrays
 */
export function arraysIntersect(array1: any[], array2: any[]): any[] {
  return array1.filter(x => array2.includes(x));
}

/**
 * Check if two arrays are the some
 * @param array1 
 * @param array2 
 * @returns If the two arrays are the same. This won't catch nested arrays or if the items in the arrays are out of order
 */
export const arraysEqual = (array1: any[], array2: any[]): boolean =>
  array1.length === array2.length &&
  array1.every((v, i) => v === array2[i]);