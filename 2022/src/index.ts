// Read in the npm attribute to get the day number we need to run
const dayNumber = process.env.npm_config_number;
if (dayNumber === undefined) {
  throw "You need to pass the day number as integer argument. ex. --day=1";
}
const exampleInput = process.env.npm_config_example_input === undefined ? false : true;


// Import the given day file and run the `solve` function on it
import(`./day${dayNumber}/solution.js`)
  .then((object) => {
    object.solve(dayNumber, exampleInput); // Hello!
  })
  .catch((error) =>
    console.log(`Could not run solver for Day ${dayNumber} | Error: ${error}`)
  );
