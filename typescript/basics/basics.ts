function add(n1: number, n2: number, showResult: boolean, phrase: string) {
  const result = n1 + n2;
  if (showResult) {
    console.log(phrase + result);
  }
  return result;
} 

const num1 = 6;
const num2 = 1.4;
const printResult = true;
const resultPhrase = "Result is ";
console.log(add(num1, num2, printResult, resultPhrase));
