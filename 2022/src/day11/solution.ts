import { performance } from 'perf_hooks';

type Primes = { [key: number]: number; };

// Set up Monkey type
type Monkey = {
  idx: number,
  activity: number,
  items: Primes[],
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

  [2].forEach(part => doIt(part));
  console.log(`Done in ${((performance.now() - st) / 1000).toFixed(4)}s`);
}

function doIt(part: number): void {
  const rounds = part === 1 ? 20 : 10000;
  // Play the 20 rounds
  for (let i = 1; i < rounds + 1; i++) {
    playRound(part);
    if ([1, 20, 1000].includes(i)) {
      console.log(`Round ${i}`);
      // monkeys.forEach(monkey => { console.log(`Monkey ${monkey.idx}: ${monkey.items.map(i => i.value)}`); });
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
    // Empty out the list of items for the Monkey
    // we do this as we don't want to alter the list while we iterate over it
    // TODO: I bet there is a better way to do this in JS... find it...

    // Loop through each item at the monkey
    while (monkey.items.length) {
      // Remove the element from the monkey
      const [item] = monkey.items.splice(0, 1);
      // console.log(`Original: ` + JSON.stringify(item, undefined, 2));
      // console.log(`Original: ` + getPrimesValue(item));
      monkey.activity++;
      // Calculate the Worry Level
      let newItem: Primes;
      /**
       * Make the `Primes` type work
       * Add to the `powers`
       * Add function that get's the values based on powers
       */
      if (monkey.operation === "*") {
        const existingPrimes = Object.keys(item).map(p => +p);
        if (monkey.operationOn === "old") {
          Object.keys(item).forEach(prime => {
            item[+prime] += item[+prime];
          });
        } else {
          if (existingPrimes.includes(+monkey.operationOn)) {
            item[+monkey.operationOn] += 1;
          } else {
            item[+monkey.operationOn] = 1;
          }
        }
        newItem = item;
      } else {
        // Addition
        let value = getPrimesValue(item);
        if (monkey.operationOn === "old") {
          value += value;
        } else {
          value += +monkey.operationOn;
        }
        newItem = getPrimeFactors(value);
      }

      if (part === 1) {
        const newValue = Math.floor(getPrimesValue(newItem) / 3);
        newItem = getPrimeFactors(newValue);
      }

      // console.log(`New: ` + getPrimesValue(newItem));
      // console.log(`New: ` + JSON.stringify(newItem, undefined, 2));
      // console.log("");

      // Check the rule and pass to the correct other monkey
      if (Object.keys(newItem).map(p => +p).includes(monkey.divisibleBy)) {
        monkeys[monkey.trueMonkeyIdx].items.push(newItem);
      } else {
        monkeys[monkey.falseMonkeyIdx].items.push(newItem);
      }
    };
  });
}

function getPrimeFactors(number: number): Primes {
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
  const primes: Primes = {};
  factors.forEach(factor => {
    factor in primes ? primes[factor] += 1 : primes[factor] = 1;
  });
  return primes;
}

function getPrimesValue(primes: Primes): number {
  let value = 1;
  for (const [prime, power] of Object.entries(primes)) {
    value *= (+prime) ** power;
  }
  return value;
}