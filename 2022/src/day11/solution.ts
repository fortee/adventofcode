import { performance } from 'perf_hooks';

// Set up Monkey type
type Monkey = {
  idx: number,
  activity: number,
  items: number[],
  operation: string,
  operationOn: string,
  divisibleBy: number,
  trueMonkeyIdx: number,
  falseMonkeyIdx: number;
};

// Main array we use to keep track of the Monkeys
const monkeys: Monkey[] = [];

// Amount we reduce the values by
const reduce = 1;

/**
 * Main function to trigger all functionality needed to solve the daily challenge
 * @param input - `raw` string content of the input file
 */
export async function solve(input: string, dayNumber: string, usingExample: boolean): Promise<void> {
  const st = performance.now();
  console.log(`---- Day ${dayNumber} ----`);


  // Pre-process the data to populate the `monkeys` array
  for (const block of input.split("Monkey ").filter(x => x !== "")) {
    const data = block.split("\n");
    monkeys.push({
      idx: +data[0].replace(":", ""),
      activity: 0,
      items: data[1].replace("Starting items: ", "").split(",").map(x => (+x.trim()) / reduce),
      operation: data[2].split("new = ")[1].split(" ")[1],
      operationOn: data[2].split("new = ")[1].split(" ")[2],
      divisibleBy: +data[3].replace("Test: divisible by ", ""),
      trueMonkeyIdx: +data[4].split("throw to monkey ")[1],
      falseMonkeyIdx: +data[5].split("throw to monkey ")[1]
    });
  }

  [2].forEach(part => doIt(part));
  console.log(`Done in ${((performance.now() - st) / 1000).toFixed(4)}s`);
}

function doIt(part: number): void {
  const rounds = part === 1 ? 20 : 10000;
  // Play the 20 rounds
  for (let i = 0; i < rounds; i++) {
    playRound(part);
    if ([1, 20, 1000].includes(i)) {
      console.log(`Round ${i}`);
      monkeys.forEach(monkey => console.log(`Monkey ${monkey.idx}: ${monkey.activity}`));
      console.log('');
    }
  }
  const result = monkeys.map(x => x.activity).sort((a, b) => b - a).slice(0, 2).reduce(function (product, value) { return product * value; });
  console.log(`Part${1}: ${result}`);
}

/**
 * Play the round where Monkeys swap items between each other
 */
function playRound(part: number): void {
  // Loop through each monkey
  monkeys.forEach(monkey => {
    const monkeyItems = [...monkey.items];
    monkey.items = [];
    // Empty out the list of items for the Monkey
    // we do this as we don't want to alter the list while we iterate over it
    // TODO: I bet there is a better way to do this in JS... find it...

    // Loop through each item at the monkey
    while (monkeyItems.length) {
      // Remove the element from the monkey
      const [item] = monkeyItems.splice(0, 1);
      monkey.activity++;
      // Calculate the Worry Level
      const calcItem = item * reduce;
      let baseWorryLevel: number;
      if (monkey.operation === "*") {
        baseWorryLevel = calcItem * (monkey.operationOn === "old" ? calcItem : +monkey.operationOn);
      } else {
        baseWorryLevel = calcItem + (monkey.operationOn === "old" ? calcItem : +monkey.operationOn);
      }

      let worryLevel: number;
      if (part === 1) {
        worryLevel = Math.floor(baseWorryLevel / 3);
      } else {
        worryLevel = baseWorryLevel;
      }

      // Check the rule and pass to the correct other monkey
      if (worryLevel % monkey.divisibleBy === 0) {
        monkeys[monkey.trueMonkeyIdx].items.push(worryLevel / reduce);
      } else {
        monkeys[monkey.falseMonkeyIdx].items.push(worryLevel / reduce);
      }
    };
  });
}