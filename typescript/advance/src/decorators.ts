function Logger(logString: string) {
    console.log("LOGGER FACTORY.........");
    return function (constructor: Function) {
      console.log("Logging........" + logString);
      console.log(constructor);
    };
  }
  
  function WithTemplate(template: string, hookId: string) {
    console.log("TEMPLATE FACTORY.........");
    return function <T extends { new (...args: any[]): { name: string } }>(
      originalConstructor: T
    ) {
      return class extends originalConstructor {
        constructor(..._: any[]) {
          super();
          console.log("rendering template........");
          const hookEl = document.getElementById(hookId);
          if (hookEl) {
            hookEl.innerHTML = template;
            hookEl.querySelector("h1")!.textContent = this.name;
          }
        }
      };
    };
  }
  
  @Logger("Logging - person")
  @WithTemplate("<h1>helooooo</h1>", "app")
  class Person {
    name = "Max";
  
    constructor() {
      console.log("Creating person object....");
    }
  }
  
  // const pers = new Person();
  // console.log(pers);
  
  function Log(target: any, propertyName: string) {
    console.log("Property decorator");
    console.log(target, propertyName);
  }
  
  function Log2(target: any, name: string, descriptor: PropertyDescriptor) {
    console.log("Accessor decorator");
    console.log(target);
    console.log(name);
    console.log(descriptor);
  }
  
  function Log3(
    target: any,
    name: string | Symbol,
    descriptor: PropertyDescriptor
  ) {
    console.log("Method decorator");
    console.log(target);
    console.log(name);
    console.log(descriptor);
  }
  
  function Log4(target: any, name: string | Symbol, position: number) {
    console.log("Parameter decorator");
    console.log(target);
    console.log(name);
    console.log(position);
  }
  
  class Prodect {
    @Log
    title: string;
    private _price: number;
  
    @Log2
    set price(val: number) {
      if (val > 0) {
        this._price = val;
      } else {
        throw new Error("Invalid price - should be positive");
      }
    }
    constructor(t: string, p: number) {
      this.title = t;
      this._price = p;
    }
  
    @Log3
    getPriceWithTax(@Log4 tax: number) {
      return this._price * (1 + tax);
    }
  }
  