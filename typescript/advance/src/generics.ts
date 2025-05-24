// const names: Array<string> = [];

// const promise: Promise<string> = new Promise((resolve, reject) => {
//   setTimeout(() => {
//     resolve("");
//   }, 2000);
// });

// promise.then((data) => {
//   data.split();
// });

function merge<T extends object, U extends object>(objA: T, objB: U) {
    return Object.assign(objA, objB);
  }
  
  const mergrObj = merge<{ name: string }, { age: number }>(
    { name: "Swaroopa" },
    { age: 20 }
  );
  console.log(mergrObj.name);
  
  interface Lengthy {
    length: number;
  }
  function countAndDescription<T extends Lengthy>(element: T): [T, string] {
    let description = "Got no value.";
    if (element.length > 0) {
      description = `Got ${element.length} element${
        element.length > 1 ? "s" : ""
      }`;
    }
    return [element, description];
  }
  
  console.log(countAndDescription(["Hi there!"]));
  
  function extractAndConvert<T extends object, U extends keyof T>(
    obj: T,
    key: U
  ) {
    return obj[key];
  }
  
  console.log(extractAndConvert({ name: "Max" }, "name"));
  
  class DataStorage<T extends string | number | boolean> {
    private data: T[] = [];
    addItem(item: T) {
      this.data.push(item);
    }
  
    removeItem(item: T) {
      this.data.splice(this.data.indexOf(item), 1);
    }
  
    getItems() {
      return [...this.data];
    }
  }
  
  const textStorage = new DataStorage<string>();
  textStorage.addItem("Max");
  textStorage.addItem("Men");
  textStorage.removeItem("Men");
  console.log(textStorage.getItems());
  
  const numbersStorage = new DataStorage<number>();
  numbersStorage.addItem(1);
  numbersStorage.addItem(2);
  numbersStorage.addItem(3);
  numbersStorage.removeItem(1);
  console.log(numbersStorage.getItems());
  
  // const objectStorage = new DataStorage<object>();
  
  // objectStorage.addItem({ name: "MAX" });
  // objectStorage.removeItem({ name: "MAX" });
  // console.log(objectStorage.getItems());
  
  interface CourseGoal {
    title: string;
    description: string;
    completeUntil: Date;
  }
  
  function createCourseGoal(
    title: string,
    description: string,
    date: Date
  ): CourseGoal {
    let courseGoal: Partial<CourseGoal> = {}; //a;; properties are optional since it is a partial type
    courseGoal.title = title;
    courseGoal.description = description;
    courseGoal.completeUntil = date;
    return courseGoal as CourseGoal;
  }
  
  const names: Readonly<string[]> = ["MAx", "Meny"];
  // names.push("sharo");
  