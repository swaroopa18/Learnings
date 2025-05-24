type Combinable = number | string;
type ConversionDescriptor = "as-number" | "as-text";

function combine(
  input1: Combinable,
  input2: Combinable,
  resultConversion: ConversionDescriptor //Literal-type
) {
  let result;
  if (
    (typeof input1 == "number" && typeof input2 == "number") ||
    resultConversion == "as-number"
  ) {
    result = +input1 + +input2;
  } else {
    result = input1.toString() + input2.toString();
  }
  return result;
}

const combineNums = combine(1, 2, "as-number");
const combineArgs = combine(1, "2", "as-number");
const combineStrings = combine("swa", "roops", "as-text");
