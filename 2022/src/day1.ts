import { readFileSync, promises as fsPromises } from "fs";
import { join } from "path";
import { urlToHttpOptions } from "url";
type inputOptions = {
  example: boolean;
  toArray: boolean;
};
function getInput(fileName: string, options: inputOptions) {
  const file = options.example ? `${fileName}_example` : fileName;
  let result = readFileSync(join(__dirname, `../src/${file}`), "utf-8");

  if (options.toArray) {
    return result.split("\n");
  }
  return result;
}

const input = getInput("/day1_input", { example: true, toArray: true });
console.log(input);
