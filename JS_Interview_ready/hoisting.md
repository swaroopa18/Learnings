# JavaScript Hoisting – 10 Interview Revision Points

### 1. What is Hoisting?
Hoisting is JavaScript's behavior of processing declarations before executing code. This makes declarations behave as if they are available at the top of their scope.

### 2. `var` Hoisting
- `var` declarations are hoisted.
- They are initialized with `undefined`.
- You can access them before their declaration without getting a ReferenceError.

```javascript
console.log(a); // undefined
var a = 10;
```

### 3. `let` Hoisting
- `let` declarations are also hoisted.
- They are not initialized until execution reaches their declaration.
- Accessing them before initialization causes a ReferenceError.

```javascript
console.log(a); // ReferenceError
let a = 10;
```

### 4. `const` Hoisting
- `const` is also hoisted.
- It remains in the Temporal Dead Zone (TDZ) until initialization.
- It must be initialized when declared.

```javascript
console.log(a); // ReferenceError
const a = 10;
```

### 5. Temporal Dead Zone (TDZ)
TDZ is the time between entering a scope and initializing a `let` or `const` variable.

Accessing these variables during the TDZ results in a ReferenceError.

### 6. Function Declaration Hoisting
- Function declarations are fully hoisted.
- You can call them before their declaration.

```javascript
greet(); // Hello

function greet() {
    console.log("Hello");
}
```

### 7. Function Expression Hoisting
- Function expressions are not fully hoisted.
- Only the variable declaration is hoisted.
- Calling a `var` function expression before assignment results in a TypeError.

```javascript
greet(); // TypeError

var greet = function() {
    console.log("Hello");
};
```

### 8. Variable Shadowing and Hoisting
A local variable with the same name as a global variable takes priority inside its scope.

```javascript
var x = 10;

function test() {
    console.log(x); // undefined
    var x = 20;
}

test();
```

### 9. Hoisting with Block Scope
- `var` is function-scoped (or globally scoped when declared outside a function).
- `let` and `const` are block-scoped.
- `var` can be accessed outside a block, while `let` and `const` cannot.

```javascript
{
    var a = 10;
    let b = 20;
}

console.log(a); // 10
console.log(b); // ReferenceError
```

### 10. Hoisting Priority and Interview Traps
- Function declarations are initialized before code execution.
- A function declaration and a `var` declaration with the same name can interact in surprising ways.
- Multiple declarations do not necessarily produce errors, but `let` and `const` cannot be redeclared in the same scope.
- Hoisting does not physically move code; it describes JavaScript's declaration processing and execution behavior.

---

## Quick Interview Cheat Sheet

| Declaration | Hoisted | Initial value | Access before declaration |
|---|---|---|---|
| `var` | Yes | `undefined` | Allowed |
| `let` | Yes | Uninitialized (TDZ) | ReferenceError |
| `const` | Yes | Uninitialized (TDZ) | ReferenceError |
| Function declaration | Yes | Function itself | Allowed |
| Function expression (`var`) | Variable only | `undefined` | Calling causes TypeError |

## One-Line Interview Answer

"Hoisting is JavaScript's behavior of processing variable and function declarations before executing the code. `var` is initialized with `undefined`, `let` and `const` remain in the Temporal Dead Zone until initialization, and function declarations are fully hoisted."

**Interview tip:** Never say JavaScript physically moves declarations to the top. Hoisting is a conceptual explanation of how JavaScript handles declarations during execution-context creation.