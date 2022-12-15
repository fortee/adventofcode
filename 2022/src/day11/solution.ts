import { performance } from 'perf_hooks';

// Set up Monkey type
type Monkey = {
  idx: number,
  activity: number,
  items: number[][],
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
    monkeys.push({
      idx: +data[0].replace(":", ""),
      activity: 0,
      items: data[1].replace("Starting items: ", "").split(",").map(x => getPrimeFactors(+x.trim())),
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
    playRound(part);
    if ([20, 1000].includes(i)) {
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
      const originalValue = item;
      monkey.activity++;
      // Calculate the Worry Level
      let newItem: number[];
      if (monkey.operation === "*") {
        if (monkey.operationOn === "old") {
          newItem = item.concat(item);

        } else {
          newItem = [...item];
          newItem.push(+monkey.operationOn);
        }
      } else {
        const itemValue = getItemValue(item);
        const newValue = itemValue + (monkey.operationOn === "old" ? itemValue : +monkey.operationOn);
        newItem = getPrimeFactors(newValue);
      }

      let newItemValue = getItemValue(newItem);
      if (part === 1) {
        newItemValue = Math.floor(newItemValue / 3);
      } else {
        newItemValue = newItemValue;
      }

      const finalItem = getPrimeFactors(newItemValue);

      // Check the rule and pass to the correct other monkey
      if (finalItem.includes(monkey.divisibleBy)) {
        monkeys[monkey.trueMonkeyIdx].items.push(finalItem);
      } else {
        monkeys[monkey.falseMonkeyIdx].items.push(finalItem);
      }
    };
  });
}

function getPrimeFactors(number: number) {
  const factors = [];
  let divisor = 2;

  while (number >= 2) {
    if (number % divisor == 0) {
      factors.push(divisor);
      number = number / divisor;
    } else {
      divisor++;
    }
  }
  return factors;
}

function getItemValue(item: number[]): number {
  return item.reduce(function (product, value) { return product * value; });
}