abstract class Department {
    //   private id: string;
    //   private name: string;
    static fiscalYear = 2020;
    protected employees: string[] = [];
    constructor(protected readonly id: string, public name: string) {
      console.log(Department.fiscalYear);
      // this.id = id;
      // this.name = n;
    }
    static createEmployee(name: string) {
      return { name: name };
    }
    abstract describe(this: Department): void;
  
    addEmployee(employee: string) {
      this.employees.push(employee);
    }
    printEmployeeInfo() {
      console.log("No of employees " + this.employees.length);
      console.log(this.employees);
    }
  }
  
  class ITDepartment extends Department {
    constructor(id: string, public admins: string[]) {
      super(id, "IT");
    }
    describe() {
      console.log("Department is:: " + this.id);
    }
  }
  const itDep = new ITDepartment("i1", ["Sweth"]);
  console.log(itDep);
  class AccountingDepartment extends Department {
    private lastReport: string;
    private static instance: AccountingDepartment;
  
    get mostRecentReport() {
      if (this.lastReport) return this.lastReport;
      throw new Error("No report found");
    }
    set mostRecentReport(value: string) {
      if (!value) throw new Error("Invalid value");
      this.addReport(value);
    }
    static getInstance() {
      if (AccountingDepartment.instance) {
        return this.instance;
      }
      this.instance = new AccountingDepartment("d2", []);
      return this.instance;
    }
    private constructor(id: string, private reports: string[]) {
      super(id, "Accouting");
      this.lastReport = reports[0];
    }
    addReport(text: string) {
      this.reports.push(text);
      this.lastReport = text;
    }
    printReports() {
      console.log(this.reports);
      console.log(this);
    }
    addEmployee(name: string) {
      if (name == "Max") {
        return;
      }
      this.employees.push(name);
    }
    describe() {
      console.log("Department is:: " + this.id);
    }
  }
  const employee1 = Department.createEmployee("Sriii");
  console.log(employee1, Department.fiscalYear);
  // const AccountingDep = new AccountingDepartment("a1", []);
  const AccountingDep = AccountingDepartment.getInstance();
  // console.log(AccountingDep.mostRecentReport);
  AccountingDep.addReport("Something is wrong");
  AccountingDep.mostRecentReport = "Nothing wrong";
  console.log(AccountingDep.mostRecentReport);
  AccountingDep.addEmployee("Swaroopa");
  AccountingDep.printReports();
  AccountingDep.describe();
  // maths.describe();
  // maths.addEmployee("Srija");
  // maths.addEmployee("Sai");
  // maths.printEmployeeInfo();
  