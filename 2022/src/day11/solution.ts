import { performance } from 'perf_hooks';

// The Monkey
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

/**
 * Main function to trigger all functionality needed to solve the daily challenge
 * @param input - `raw` string content of the input file
 */
export async function solve(input: string, dayNumber: string, usingExample: boolean): Promise<void> {
  const st = performance.now();
  console.log(`---- Day ${dayNumber} ----`);
  [1, 2].forEach(part => doIt(input, part));
  console.log(`Done in ${((performance.now() - st) / 1000).toFixed(4)}s`);
}

function doIt(input: string, part: number): void {
  const [monkeys, lcd] = getMonkeyData(input);
  const rounds = part === 1 ? 20 : 10000;
  // Play the round for the part
  for (let i = 1; i < rounds + 1; i++) {
    playRound(monkeys, lcd, part);
  }
  const result = monkeys.map(x => x.activity).sort((a, b) => b - a).slice(0, 2).reduce(function (product, value) { return product * value; });
  console.log(`Part${1}: ${result}`);
}

/**
 * Play the round where Monkeys swap items between each other
 */
function playRound(monkeys: Monkey[], lcd: number, part: number): void {
  // Loop through each monkey
  monkeys.forEach(monkey => {
    // Loop through each item at the monkey
    while (monkey.items.length > 0) {

      // Remove the element from the monkey
      const [item] = monkey.items.splice(0, 1);

      // Update the Monkey activity
      monkey.activity++;

      // Calculate the Worry Level
      const value = (monkey.operationOn === "old" ? item : +monkey.operationOn);
      const baseWorryLevel = monkey.operation === "*" ? item * value : item + value;

      let worryLevel: number;
      if (part === 1) {
        worryLevel = Math.floor(baseWorryLevel / 3);
      } else {
        /**
         * Use `Least Common Denominator` to reduce the number
         * Ex. Check division for 3, 7 for number 2187:
         *      lcd = 21 (3*7)
         *      baseWorryLevel = 27
         *      2187 / 21 = 104,142857143 => Math.floor(2187 / 21) = 104
         *      104 * lcd = 2184
         *      2187 - 2184 = 3
         *      At this point we have "split" the original number (the number we want to "reduce") to 2184 and 3
         *      We know that `2184` is divisible with both 7 and 3, which means we only need to investigate the divisibility of the remainder
         *      3 % 3 === 0 will be the same as 2187 % 3 === 0
         *      3 % 7 === 0 will be the same as 2187 % 7 === 0
         *      This means we can pass the remainder along as a new item for the next Monkey, instead of the ever growing number
         */
        worryLevel = baseWorryLevel > lcd ? baseWorryLevel - (Math.floor(baseWorryLevel / lcd) * lcd) : baseWorryLevel;
      }

      // Check the rule and pass to the correct other monkey
      if (worryLevel % monkey.divisibleBy === 0) {
        monkeys[monkey.trueMonkeyIdx].items.push(worryLevel);
      } else {
        monkeys[monkey.falseMonkeyIdx].items.push(worryLevel);
      }

    };
  });
}

/**
 * Get the Monkey data by parsing the input
 * @param input - The Input
 */
function getMonkeyData(input: string): [Monkey[], number] {
  let lcd = 1;
  let monkeys: Monkey[] = [];
  // Pre-process the data to populate the `monkeys` array
  for (const block of input.split("Monkey ").filter(x => x !== "")) {
    const data = block.split("\n");
    const divisible = +data[3].replace("Test: divisible by ", "");
    monkeys.push({
      idx: +data[0].replace(":", ""),
      activity: 0,
      items: data[1].replace("Starting items: ", "").split(",").map(x => +x.trim()),
      operation: data[2].split("new = ")[1].split(" ")[1],
      operationOn: data[2].split("new = ")[1].split(" ")[2],
      divisibleBy: divisible,
      trueMonkeyIdx: +data[4].split("throw to monkey ")[1],
      falseMonkeyIdx: +data[5].split("throw to monkey ")[1]
    });
    lcd *= divisible;
  }
  return [monkeys, lcd];
}