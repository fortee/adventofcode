import { performance } from 'perf_hooks';

/**
 * Main function to trigger all functionality needed to solve the daily challenge
 * @param input - `raw` string content of the input file
 */
export async function solve(input: string, dayNumber: string, usingExample: boolean): Promise<void> {
  const st = performance.now();
  console.log(`---- Day ${dayNumber} ----`);

  // Split the string to an array of items
  const inputArray = input.split("\n");

  // Calculate the edges of the area
  const gridWidth = inputArray[0].length;
  const gridHeight = inputArray.length;
  let visibleTrees = (gridWidth * 2) + (gridHeight * 2) - 4;
  const scenicScores: number[] = [];

  // Pre-process the input so we have a 2d array of numbers for both rows and columns
  // This should will speed up the later column lookup
  const columns: Record<number, number[]> = {};
  const rows: number[][] = [];
  inputArray.forEach(function (line) {
    const row = line.split("").map(x => +x);
    rows.push(row);
    row.forEach(function (tree, x) {
      columns[x] ? columns[x].push(tree) : columns[x] = [tree];
    });
  });

  // Loop over the whole area again
  rows.forEach(function (row, y) {

    // We don't want to investigate the first and last row in the area
    if ([0, inputArray.length - 1].includes(y)) return;

    row.forEach(function (tree, x) {

      // We don't want to investigate the first and last column in the area
      if ([0, row.length - 1].includes(x)) return;

      // Find the correct column
      const column = columns[x];

      // Find the trees in each direction
      const up = column.slice(0, y).reverse();  // Reverse as we we are looking from our tree outwards over this array of trees
      const left = row.slice(0, x).reverse(); // Reverse as we we are looking from our tree outwards over this array of trees
      const down = column.slice(y + 1);
      const right = row.slice(x + 1);

      // Set default for the variables
      let currentTreeVisible = false;
      const viewDistances: number[] = [];

      for (const direction of [up, down, left, right]) {
        // Loop through each direction

        // Part 1 solution
        if (Math.max(...direction) < tree) currentTreeVisible = true;

        // Part 2 solution
        let viewDistance = 0;
        let viewBlocked = false;
        for (const otherTree of direction) {
          // Loop through each tree in the direction

          if (viewBlocked) continue; // If the view was already blocked that is nothing else to do
          viewDistance++; // Count-up the viewing distance
          if (otherTree >= tree) viewBlocked = true; // If the tree is blocking our view
        }

        // Keep track of the viewing distance for this direction
        viewDistances.push(viewDistance);
      }

      // (Part1) If the current Tree is visible up-count the number of total visible trees
      if (currentTreeVisible) visibleTrees++;

      // (Part2) A tree's scenic score is found by multiplying together its viewing distance in each of the four directions.
      const treeScenicScore = viewDistances.reduce(function (product, value) { return product * value; });

      // (Part2) Keep track of each tree's scenic score
      scenicScores.push(treeScenicScore);

    });
  });

  console.log(`Part1: ${visibleTrees}`);
  console.log(`Part2: ${Math.max(...scenicScores)}`); input;

  console.log(`Done in ${((performance.now() - st) / 1000).toFixed(4)}s`);
}