# Prototypal Inheritance in JavaScript

## 1. What is prototypal inheritance?

Prototypal inheritance is JavaScript's mechanism for allowing an object to access properties and methods from another object through its **prototype**.

In simple terms, an object can reuse another object's properties and methods without copying them.

```js
const person = {
  greet() {
    console.log("Hello!");
  }
};

const user = {
  name: "John"
};

Object.setPrototypeOf(user, person);

user.greet(); // "Hello!"
console.log(user.name); // "John"
```

- `person` owns the `greet()` method.
- `user` does not have its own `greet()` method.
- JavaScript looks up `user`'s prototype and finds `greet()` on `person`.

> Note: `Object.setPrototypeOf()` is useful for demonstrating the concept, but changing an object's prototype after creation can hurt performance. Prefer creating objects with the intended prototype from the start.

## 2. The prototype chain

When JavaScript reads a property, it searches in this order:

1. Check the object itself.
2. If the property is not found, check the object's prototype.
3. Continue checking each prototype's prototype.
4. Stop when the property is found or the chain reaches `null`.

```js
const animal = {
  eat() {
    console.log("Eating...");
  }
};

const dog = {
  bark() {
    console.log("Barking...");
  }
};

Object.setPrototypeOf(dog, animal);

dog.bark(); // "Barking..."
dog.eat();  // "Eating..."
```

The lookup path is:

```text
dog
  |
  v
animal
  |
  v
Object.prototype
  |
  v
null
```

The exact chain depends on how the objects were created. In this example, `animal` itself inherits from `Object.prototype`.

## 3. `[[Prototype]]`, `__proto__`, and prototype methods

- `[[Prototype]]` is the internal link an object uses to refer to its prototype.
- `__proto__` is a legacy accessor that exposes that link.
- Prefer `Object.getPrototypeOf()` to read an object's prototype.
- Use `Object.create()` to create an object with a chosen prototype.

```js
const parent = { role: "admin" };
const child = Object.create(parent);

console.log(Object.getPrototypeOf(child) === parent); // true
console.log(child.role); // "admin"
```

To set a prototype explicitly:

```js
Object.setPrototypeOf(child, parent);
```

## 4. `prototype` on constructor functions

A normal constructor function has a `prototype` property. When it is called with `new`, the new object's internal prototype is linked to the constructor's `prototype` object.

```js
function Person(name) {
  this.name = name;
}

Person.prototype.greet = function () {
  console.log("Hello, " + this.name);
};

const user1 = new Person("John");
const user2 = new Person("David");

user1.greet(); // "Hello, John"
user2.greet(); // "Hello, David"
```

Both instances can use the same `greet` function through their prototype. The method is not copied onto each instance.

## 5. `prototype` vs `__proto__`

| `prototype` | `__proto__` |
|---|---|
| A property found on constructor functions (and other functions) | A legacy accessor available on objects through `Object.prototype` |
| Used as the prototype for instances created with `new` | Reads or sets the object's internal prototype |
| Example: `Person.prototype` | Example: `user.__proto__` |

Preferred modern check:

```js
function Person() {}

const user = new Person();

console.log(Object.getPrototypeOf(user) === Person.prototype);
// true
```

Remember: `prototype` and `[[Prototype]]` are related, but they are not the same thing.

## 6. `Object.create()`

`Object.create(proto)` creates a new object whose prototype is `proto`.

```js
const person = {
  greet() {
    console.log("Hello!");
  }
};

const user = Object.create(person);

user.greet(); // "Hello!"
```

This is a direct way to establish prototypal inheritance without using a constructor function.

## 7. Method overriding and property shadowing

If an object has its own property with the same name as an inherited property, JavaScript uses the object's own property first. This is called **property shadowing**.

```js
const parent = {
  greet() {
    console.log("Parent greeting");
  }
};

const child = Object.create(parent);

child.greet = function () {
  console.log("Child greeting");
};

child.greet(); // "Child greeting"
```

The parent's method still exists; it is simply shadowed by the child's own method.

## 8. Built-in prototypes

JavaScript's built-in objects also use prototypes.

For example, arrays inherit methods such as `map()`, `filter()`, and `reduce()` from `Array.prototype`.

```js
const numbers = [1, 2, 3];

console.log(Object.getPrototypeOf(numbers) === Array.prototype);
// true

console.log(numbers.map(n => n * 2)); // [2, 4, 6]
```

The array can use these methods because of its prototype chain.

## 9. JavaScript classes and prototypal inheritance

JavaScript classes provide cleaner syntax for constructor functions and prototype-based inheritance. The methods declared in a class body are placed on the class's prototype.

```js
class Animal {
  speak() {
    console.log("Animal sound");
  }
}

class Dog extends Animal {
  bark() {
    console.log("Woof!");
  }
}

const dog = new Dog();

dog.bark();  // "Woof!"
dog.speak(); // "Animal sound"
```

`Dog` inherits from `Animal`. The `extends` syntax uses JavaScript's prototype mechanism.

## 10. Real-world use cases

1. **Code reuse:** Share common methods across many objects.
2. **Memory efficiency:** Put shared methods on a prototype instead of creating a new function for every instance.
3. **Inheritance:** Model relationships such as `Animal` → `Dog`.
4. **Built-in functionality:** Arrays, dates, and other built-in objects use prototype methods.
5. **Class inheritance:** `extends` and `super` work with the prototype-based inheritance system.

## 11. Ten interview points to remember

1. JavaScript uses prototypal inheritance.
2. Objects have an internal `[[Prototype]]` link.
3. An object can access properties and methods from its prototype.
4. JavaScript searches the prototype chain when a property is not found on the object itself.
5. The prototype chain ends at `null`.
6. `Object.getPrototypeOf(obj)` reads an object's prototype.
7. `Object.create(proto)` creates an object with the specified prototype.
8. Constructor functions have a `prototype` property.
9. Instances created with `new` are linked to the constructor's `prototype`.
10. JavaScript classes use the prototype system under the hood.

## 12. Common interview questions

### Q1. What is prototypal inheritance?

It is a JavaScript mechanism where an object inherits properties and methods from another object through its prototype.

### Q2. What is the prototype chain?

It is the sequence of prototype links JavaScript follows when looking up a property. The search ends when the property is found or the chain reaches `null`.

### Q3. What is the difference between `prototype` and `__proto__`?

`prototype` is a property on constructor functions that becomes the prototype of instances created with `new`. `__proto__` is a legacy accessor for an object's internal prototype. Prefer `Object.getPrototypeOf()` for reading it.

### Q4. How do you create an object with another object as its prototype?

Use `Object.create()`:

```js
const child = Object.create(parent);
```

### Q5. What happens if both an object and its prototype have a property with the same name?

The object's own property takes precedence. It shadows the inherited property.

### Q6. Do JavaScript classes use prototypal inheritance?

Yes. Class syntax is built on JavaScript's prototype system. Methods declared in a class body are placed on its prototype.

## 13. Practice questions

Try to predict each output before running the code.

### Question 1

```js
const parent = { name: "John" };
const child = Object.create(parent);

console.log(child.name);
```

**Answer:** `"John"` — JavaScript finds `name` on the prototype.

### Question 2

```js
const parent = { age: 40 };
const child = Object.create(parent);

child.age = 20;

console.log(child.age);
console.log(parent.age);
```

**Answer:**
```text
20
40
```

The child's own `age` property shadows the inherited one. The parent is unchanged.

### Question 3

```js
function User() {}

const user = new User();

console.log(Object.getPrototypeOf(user) === User.prototype);
```

**Answer:** `true` — `new User()` links the new object's prototype to `User.prototype`.

### Question 4

```js
const animal = {
  speak() {
    return "Animal sound";
  }
};

const dog = Object.create(animal);

dog.speak = function () {
  return "Woof!";
};

console.log(dog.speak());
```

**Answer:** `"Woof!"` — the own method shadows the inherited method.

---

## Quick revision

- **Prototype:** The object another object delegates property lookups to.
- **Prototype chain:** The linked sequence of prototypes used for property lookup.
- **`[[Prototype]]`:** The internal prototype link.
- **`prototype`:** A property on constructor functions used when creating instances with `new`.
- **`Object.create()`:** Creates an object with a chosen prototype.
- **Shadowing:** An object's own property takes precedence over an inherited property.
- **Classes:** A convenient syntax built on prototypal inheritance.
