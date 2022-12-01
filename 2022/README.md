# Advent Of Code 2022
https://adventofcode.com/2022

## Run solution for a given day

Run with `npm run solve --number={day number}` ex.: `npm run solve --number=1`
add `--example-input` to run the code with the example inputs ex.: `npm run solve --number=1 --example-input`

## Add new day solution

- Add new folder under `src` named `day{number}` ex: `day3`
- Create new file called `solution.ts` that should contain a `export async function solve(input: string, dayNumber: string) {}` method. This will be called when the `solve` npm script is triggered
- Add two new files `input` and `input_example` that should contain the provided puzzle input

## Utils

Common functionality between daily solutions are maintained in `./utils` folder
