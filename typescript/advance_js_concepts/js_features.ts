const add = (a: number, b: number = 4) => a + b;
// const printResult = (output: number | string) => console.log(output);
type printResultFunc = (o: number | string) => void;
const printResult: printResultFunc = (output) => console.log(output);

const hobbies: string[] = ["cooking", "reading", "playing badmintion"];
let activeHobbies = [...hobbies];
activeHobbies.push(hobbies[0]);

const addition = (...numbers: number[]) => {
  return numbers.reduce(
    (currentResult, currentVal) => currentResult + currentResult,
    0
  );
};

console.log(addition(1, 2, 3, 4, 5));

//Array destructuring

const [hobby1, hobby2, ...remaningHobbies] = hobbies;

console.log(hobby1, hobby2, remaningHobbies, hobbies);
