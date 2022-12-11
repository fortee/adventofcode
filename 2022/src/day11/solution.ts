import { performance } from 'perf_hooks';

type Item = {
  base: number,
  multiply: number[],
  added: number;
};

/**
 * Get the item value
 * @param item 
 * @returns 
 */
function getItemValue(item: Item): number {
  let value = item.base;
  item.multiply.forEach(amount => {
    value *= amount;
  });
  return Math.round(value + item.added);
}

// Set up Monkey type
type Monkey = {
  idx: number,
  activity: number,
  items: Item[],
  operation: string,
  operationOn: string,
  divisibleBy: number,
  trueMonkeyIdx: number,
  falseMonkeyIdx: number;
};

// Main array we use to keep track of the Monkeys
const monkeys: Monkey[] = [];

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
    const items: Item[] = [];
    for (const item of data[1].replace("Starting items: ", "").split(",")) {
      items.push({
        base: +item.trim(),
        multiply: [],
        added: 0,
      });
    }
    monkeys.push({
      idx: +data[0].replace(":", ""),
      activity: 0,
      items: items,
      operation: data[2].split("new = ")[1].split(" ")[1],
      operationOn: data[2].split("new = ")[1].split(" ")[2],
      divisibleBy: +data[3].replace("Test: divisible by ", ""),
      trueMonkeyIdx: +data[4].split("throw to monkey ")[1],
      falseMonkeyIdx: +data[5].split("throw to monkey ")[1]
    });
  }

  [1].forEach(part => doIt(part));
  console.log(`Done in ${((performance.now() - st) / 1000).toFixed(4)}s`);
}

function doIt(part: number): void {
  const rounds = part === 1 ? 20 : 10000;
  // Play the 20 rounds
  for (let i = 1; i < rounds + 1; i++) {
    playRound(part, i);
    // if ([1, 20, 1000].includes(i)) {
    console.log(`Round ${i}`);
    monkeys.forEach(monkey => {
      console.log(`Monkey ${monkey.idx}: ${monkey.items.map(item => getItemValue(item))}`);
    });
    // monkeys.forEach(monkey => console.log(`Monkey ${monkey.idx}: ${monkey.activity}`));
    console.log('');
    // }
  }
  const result = monkeys.map(x => x.activity).sort((a, b) => b - a).slice(0, 2).reduce(function (product, value) { return product * value; });
  console.log(`Part${1}: ${result}`);
}

/**
 * Play the round where Monkeys swap items between each other
 */
function playRound(part: number, round: number): void {
  // Loop through each monkey
  monkeys.forEach(monkey => {
    const monkeyItems = [...monkey.items];
    console.log(`Monkey ${monkey.idx}`);
    
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
      if (monkey.operation === "*") {
        item.multiply.push(monkey.operationOn === "old" ? item.base : +monkey.operationOn);
      } else {
        item.added += (monkey.operationOn === "old" ? item.base : +monkey.operationOn);
      }

      // Get the current Item value
      const currentItemValue = getItemValue(item);

      let worryLevel: number;
      if (part === 1) {
        worryLevel = Math.floor(currentItemValue / 3);
      } else {
        worryLevel = currentItemValue;
      }

      const newItem = {
        base: worryLevel / 10000,
        multiply: [10000],
        added: 0
      };

      // Check the rule and pass to the correct other monkey
      if (worryLevel % monkey.divisibleBy === 0) {
        monkeys[monkey.trueMonkeyIdx].items.push(newItem);
      } else {
        monkeys[monkey.falseMonkeyIdx].items.push(newItem);
      }
    };
  });
}