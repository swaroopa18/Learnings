function add(n1: number, n2: number): number {
    return n1 + n2;
  }
  
  function printResult(num: number): void {
    console.log("Result..." + num);
  }
  
  let combineValues: (a: number, b: number) => number;
  let display: (a: number) => void;
  
  combineValues = add;
  display = printResult;
  console.log(combineValues(1, 2));
  console.log(display(1));
  
  function addAndHandle(n1: number, n2: number, cb: (result) => void): void {
    cb(n1 + n2);
  }
  
  addAndHandle(10, 12, (result: number) => {
    console.log(result);
  });
  