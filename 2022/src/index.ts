import { getInput } from "./utils/tools";


// Read in the npm attributes

// Represents the number of the day we should run
const dayNumber = process.env.npm_config_number;
if (dayNumber === undefined) {
  // Make this attribute required
  throw "You need to pass the day number as integer argument. ex. --day=1";
}


// Represents if we should use the normal or example inputs
const exampleInput =
  process.env.npm_config_ex === undefined ? false : true;

// Import the given day's solution file and run the `solve` function on it
import(`./day${dayNumber}/solution.js`)
  .then((object) => {
    const input: string = getInput({
      dayNumber: dayNumber,
      example: exampleInput,
    });
    // Run the solve() function to get the given day's solution
    object.solve(input, dayNumber, exampleInput);
  })
  .catch((error) =>
    // Something is wrong
    console.error(`Could not run solver for Day ${dayNumber} | Error: ${error}`)
  );
