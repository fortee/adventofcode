import { readFileSync, promises as fsPromises } from "fs";
import { join } from "path";

type inputOptions = {
  dayNumber: string;
  example: boolean;
};

export function getInput(options: inputOptions): string {
  const file = options.example ? "input_example" : "input";
  return readFileSync(
    join(__dirname, `../../src/day${options.dayNumber}/${file}`),
    "utf-8"
  );
}
