import { performance } from 'perf_hooks';

// Type we will use to define directory objects
type dir = {
  name: string,
  parent: dir | undefined,
  children: dir[],
  files: string[],
  size: number,
};

// Define the root directory
let rootDirectory: dir = {
  name: 'root',
  // The root dir doesn't have a parent
  parent: undefined,
  children: [],
  files: [],
  size: 0
};

// The total disk space available to the filesystem is 70000000.
const totalSpace = 70000000;
// To run the update, you need unused space of at least 30000000.
const neededFreeSpace = 30000000;

// Initialize default variables
let part1Solution = 0;
let currentFreeSpace = 0;
let part2Solution: number | undefined = undefined;


/**
 * Main function to trigger all functionality needed to solve the daily challenge
 * @param input - `raw` string content of the input file
 */
export async function solve(input: string, dayNumber: string, usingExample:boolean) {
  const st = performance.now();
  console.log(`---- Day ${dayNumber} ----`);

  // Split the string to an array of items
  const inputArray = input.split("\n");

  // We can remove the first two lines
  inputArray.splice(0, 2);

  // Build the directory tree
  createDirectoryTree(inputArray);

  // Once the directory tree is created the root directory should have it's size set correctly
  currentFreeSpace = totalSpace - rootDirectory.size;

  // Traverse the tree to calculate the puzzle solutions
  traverseDirectoryTree();

  // Print the results
  console.log(`Part1: ${part1Solution}`);
  console.log(`Part2: ${part2Solution}`);

  console.log(`Done in ${((performance.now() - st) / 1000).toFixed(2)}s`);
}

/**
 * Create the directory tree based on the input
 * @param input 
 */
function createDirectoryTree(input: string[]): void {

  // Manually set the root dir as the current starting dir
  let currentDirectory = rootDirectory;

  for (const line of input) {
    // Loop trough the input

    // Get the line data
    const lineData = line.split(" ");

    switch (lineData[0]) {
      // Run different functionality depending on the first word 
      case "$":
        // This is some kind of command

        if (lineData[1] == "cd" && lineData[2] == ".." && currentDirectory.parent !== undefined) {
          // Move up one level
          // If the current directory has a parent directory move up to it
          if (currentDirectory.parent !== undefined) currentDirectory = currentDirectory.parent;
          break;
        }

        // Try to find the directory between the children of the current directory
        const targeDirectory = currentDirectory.children.find(d => d.name === lineData[2]);

        if (lineData[1] == "cd" && targeDirectory !== undefined) {
          // Move to the given directory if it already exists as child under the current directory
          currentDirectory = targeDirectory;
          break;
        }

        // We don't need to worry about the rest of the commands
        break;
      case "dir":
        // The content of the current directory contains another directory
        createNewDirectory(lineData[1], currentDirectory);
        break;
      default:
        // The content of the current directory contains a file
        updateDirectorySizeWithFileSize(currentDirectory, +lineData[0]);
        currentDirectory.files.push(line);
        break;
    }
  }
}

/**
 * Create a new directory
 * @param directoryName - Name of the new directory
 * @param parentDirectory - Parent directory of the newly created directory
 */
function createNewDirectory(directoryName: string, parentDirectory: dir): void {

  // Check if the given parent directory already has a child directory with the given name
  const childWithNameExists = parentDirectory.children.find(d => d.name === directoryName);
  if (childWithNameExists !== undefined) {
    // We should not try add the same child directory again
    // This could happen as the `createNewDirectory` is triggered each time we encounter this directory during an `ls`
    return;
  }

  // Create the new directory
  const directory: dir = {
    name: directoryName,
    parent: parentDirectory,
    children: [],
    files: [],
    size: 0
  };

  // Add the new dir as a child to the parent dir
  parentDirectory.children.push(directory);
}

/**
 * Update the size of the directory, and it's parents recursively
 * TODO:  This is not the most efficient, as for each file we traverse up the child-parent hierarchy
 *        We could achieve the same thing quicker by adding up the child directory sizes when we traverse the final tree.
 * @param directory - The directory we want to update
 * @param size - The size of the file
 */
function updateDirectorySizeWithFileSize(directory: dir, size: number): void {
  directory.size += size;
  if (directory.parent !== undefined) {
    updateDirectorySizeWithFileSize(directory.parent, size);
  }
}

/**
 * Traverse the whole tree so we can account for the different puzzle solutions
 */
function traverseDirectoryTree(): void {
  traverseChildDirectories(rootDirectory.children);
}

/**
 * Recursively traverse the given child directories
 * @param directories 
 */
function traverseChildDirectories(directories: dir[]): void {

  for (const directory of directories) {
    // Loop over all directories

    // Account for part1 solution
    if (directory.size <= 100000) part1Solution += directory.size;

    // Account for part2 solution
    if (directory.size >= (neededFreeSpace - currentFreeSpace) && (part2Solution === undefined || directory.size < part2Solution)) {
      // If the current directories size is big enough to account for the total remaining space we need to gain
      // and we don't have a directory candidate yet, or that candidate's size is bigger than that of the current directory
      part2Solution = directory.size;
    }

    // Traverse the current directories children
    traverseChildDirectories(directory.children);
  }
}