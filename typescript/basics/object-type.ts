enum Responsibility {
  ADMIN,
  READ_ONLY,
  AUTHOR,
}
type Person = {
  name: string;
  age: number;
  hobbies: string[];
  favouriteThings: any[];
  // role: (string | number)[];
  role: [number | string, number | string];
  responsibility: Responsibility;
};
const person: Person = {
  name: "Swaroopa",
  age: 24,
  hobbies: ["Sports", "Cooking"],
  favouriteThings: [1, "S", 1.2, true],
  role: ["23", 2],
  responsibility: Responsibility.ADMIN,
};

for (const hobby of person.hobbies) {
  console.log(hobby.toUpperCase());
}
