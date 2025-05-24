type Admin = {
    name: string;
    privilages: string[];
  };
  
  type Employee = {
    name: string;
    startDate: Date;
  };
  
  type ElevatedEmployee = Admin & Employee;
  
  const e1: ElevatedEmployee = {
    name: "Swaroopa",
    startDate: new Date(),
    privilages: [],
  };
  
  type Combinable = string | number;
  type Numeric = number | boolean;
  
  type Universal = Combinable & Numeric;
  
  function add(a: string, b: number): number;
  function add(a: string, b: string): string;
  function add(a: number, b: number): number;
  function add(a: Combinable, b: Combinable) {
    if (typeof a === "string" || typeof b === "string") {
      return a.toString() + b.toString();
    }
    return a + b;
  }
  // const sum = add(1, 3) as number;
  const sum = add("sw", "ws") as string;
  // sum.split("")
  
  // type UnknownEmployee = Employee | Admin;
  
  // function printEmployeeInformation(emp: UnknownEmployee) {
  //   console.log("Name" + emp.name);
  //   if ("privilages" in emp) {
  //     console.log("Privilages" + emp.privilages);
  //   }
  //   //   if (emp instanceof Admin) {
  //   //     console.log("Privilages" + emp.privilages);
  //   //   }
  //   if ("startDate" in emp) {
  //     console.log("StartDate" + emp.startDate);
  //   }
  // }
  
  // printEmployeeInformation({ name: "Swaroopa", startDate: new Date() });
  
  // class Car {
  //   drive() {
  //     console.log("Driving.....");
  //   }
  // }
  
  // class Truck {
  //   drive() {
  //     console.log("Driving a truck.....");
  //   }
  //   loadCargo(amount: number) {
  //     console.log("Loading a cargo....." + amount);
  //   }
  // }
  
  // type Vehicle = Car | Truck;
  
  // const v1 = new Car();
  // const v2 = new Truck();
  
  // function useVehicle(vehicle: Vehicle) {
  //   vehicle.drive();
  
  //   //   if ("loadCargo" in vehicle) {
  //   //     vehicle.loadCargo(1000);
  //   //   }
  //   if (vehicle instanceof Truck) {
  //     vehicle.loadCargo(1000);
  //   }
  // }
  
  // useVehicle(v1);
  // useVehicle(v2);
  
  // //Discriminated unions
  // interface Bird {
  //   type: "bird";
  //   flyingSpeed: number;
  // }
  
  // interface Horse {
  //   type: "horse";
  //   runningSpeed: number;
  // }
  
  // type Animal = Bird | Horse;
  
  // function moveAnimal(animal: Animal) {
  //   let speed;
  //   switch (animal.type) {
  //     case "bird":
  //       speed = animal.flyingSpeed;
  //       break;
  //     case "horse":
  //       speed = animal.runningSpeed;
  //   }
  //   console.log("Speed----->" + speed);
  // }
  
  // moveAnimal({ type: "bird", flyingSpeed: 100 });
  
  // const paragraph1 = document.getElementById("message-output");
  // // const userinput = <HTMLInputElement>document.getElementById("user-input")!;
  // const userinput = document.getElementById("user-input") as HTMLInputElement;
  // if (userinput.value) userinput.value = "Hi There"!;
  
  // interface ErrorContainer {
  //   [prop: string]: string;
  // }
  
  // const error: ErrorContainer = {
  //   true: "Not a valid type",
  //   1: "rwet",
  //   2: "er",
  //   email: "",
  // };
  
  //Optional chaining
  const fetchedUSer = {
    id: "u1",
    name: "Swaroopa",
    job: { title: "SCP", desc: "I am a developer" },
  };
  
  console.log(fetchedUSer.job.desc);
  console.log(fetchedUSer?.job?.desc);
  
  //Nullish coalescing
  const userInput = null;
  const storedData = userInput || "DEFAULT";
  