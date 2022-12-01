import { join } from "path";
import { readFileSync } from "fs";

/**
 * The options we accept for the getInput() method
 */
type getInputOptions = {
  dayNumber: string;
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
