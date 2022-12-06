/**
 * Main function to trigger all functionality needed to solve the daily challenge
 * @param input - `raw` string content of the input file
 */
export async function solve(input: string, dayNumber: string) {
  console.log(`---- Day ${dayNumber} ----`);

  // Split the string to an array of items
  const inputArray = input.split("\n").map((x) => x.split(" "));

  // Solve Part 1 & 2
  [1, 2].forEach((part) => {
    solveIt(inputArray, part);
  });
}

// Convert the enemy an own choice to more descriptive letter
const converter: Record<string, string> = {
  A: "R",
  B: "P",
  C: "S",
  X: "R",
  Y: "P",
  Z: "S",
};

// Hard code the points for our choice
const pointsForChoice: Record<string, number> = {
  R: 1,
  P: 2,
  S: 3,
};

// Hard code the results
const getResultPoint: Record<string, number> = {
  RP: 6,
  RR: 3,
  RS: 0,
  PS: 6,
  PP: 3,
  PR: 0,
  SR: 6,
  SS: 3,
  SP: 0,
};

// Hard code the results
const resultToPoint: Record<string, number> = {
  R: 0,
  P: 3,
  S: 6,
};

/**
 * @param input - The Puzzle input
 * @param part - Which part we are solving
 */
function solveIt(input: string[][], part: number) {
  // Keep track of the total points for the part
  let totalPoints = 0;

  input.forEach((round) => {
    // Get the choice of our enemy with a more descriptive letter we can use for other decoding
    const enemyChoice: string = converter[round[0]];

    // Get our own choice with a more descriptive letter we can use for other decoding
    let ourChoice = converter[round[1]];
    if (part === 2) {
      // For part 2 we need apply the logic that gets us our choice based on the result we need

      // Find what point we need
      const pointWeNeed = resultToPoint[ourChoice];

      // Loop through the `getResultPoint`
      // Find ones that have the correct result and enemy choice
      const correctPairs = Object.keys(getResultPoint).filter(
        (key) => key[0] === enemyChoice && getResultPoint[key] === pointWeNeed
      );

      // We found a correct pair, we need the second string, which is our choice
      ourChoice = correctPairs[0][1];
    }

    // The points we get for our own choice
    const choicePoint = pointsForChoice[ourChoice];

    // The points we get for the results of this round
    const resultPoint = getResultPoint[`${enemyChoice}${ourChoice}`];

    // Add the sum of the two points
    totalPoints += choicePoint + resultPoint;
  });
  console.log(`Part${part}: ${totalPoints}`);
}
