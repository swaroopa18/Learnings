# Python Abstraction – Complete Notes (Beginner to Senior Level)

## 1. What is Abstraction?

Abstraction is one of the four pillars of Object-Oriented Programming (OOP).

**Definition:** Abstraction is the process of hiding internal implementation details and exposing only essential functionality to the user.

In simple words:

- Focus on WHAT an object does.
- Hide HOW the object does it.

### Real-world example: ATM

When using an ATM:
- Insert your card.
- Enter your PIN.
- Enter the withdrawal amount.
- Receive money.

You don't need to know how the ATM communicates with the bank server or processes the transaction internally.

This is abstraction.

---

## 2. Abstraction in Python

Python provides abstraction using the `abc` module.

ABC stands for Abstract Base Class.

Important components:

- `ABC`: Abstract Base Class.
- `@abstractmethod`: Defines an abstract method.
- Concrete method: A method with an implementation.
- Abstract method: A method declared in an abstract class that must be implemented by concrete subclasses.

### Syntax

```python
from abc import ABC, abstractmethod

class Parent(ABC):

    @abstractmethod
    def method(self):
        pass


class Child(Parent):

    def method(self):
        print("Implementation in child class")


obj = Child()
obj.method()
```

Output:

```text
Implementation in child class
```

### Important points

1. An abstract class can contain abstract methods.
2. It can also contain normal methods.
3. It can have constructors.
4. It can have attributes.
5. It cannot be instantiated while it has unimplemented abstract methods.
6. A concrete child class must implement all inherited abstract methods.

---

## 3. Can We Instantiate an Abstract Class?

This is one of the most important concepts.

### Case 1: Abstract class with an abstract method

```python
from abc import ABC, abstractmethod

class Animal(ABC):

    @abstractmethod
    def sound(self):
        pass


animal = Animal()
```

Output:

```text
TypeError: Can't instantiate abstract class Animal
```

Why?

Because `sound()` is an abstract method and has not been implemented.

### Case 2: Instantiate using a child class

```python
from abc import ABC, abstractmethod

class Animal(ABC):

    @abstractmethod
    def sound(self):
        pass


class Dog(Animal):

    def sound(self):
        print("Dog barks")


dog = Dog()
dog.sound()
```

Output:

```text
Dog barks
```

The child class implements the abstract method, so its object can be created.

### Case 3: Abstract class without abstract methods

```python
from abc import ABC

class Employee(ABC):

    def __init__(self, name):
        self.name = name


emp = Employee("Rahul")

print(emp.name)
```

Output:

```text
Rahul
```

**Important:** An ABC without any abstract methods can be instantiated.

The `ABC` inheritance alone does not prevent object creation.

---

## 4. Can Abstract Classes Have Attributes?

Yes! Abstract classes can have all the attributes that normal classes have.

### 4.1 Instance attributes

```python
from abc import ABC, abstractmethod

class Employee(ABC):

    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    @abstractmethod
    def calculate_salary(self):
        pass


class Developer(Employee):

    def calculate_salary(self):
        return self.salary


dev = Developer("Rahul", 50000)

print(dev.name)
print(dev.salary)
```

Output:

```text
Rahul
50000
```

Here:
- `name` is an instance attribute.
- `salary` is an instance attribute.
- Both are defined in the abstract parent class.
- The child class inherits them.

### 4.2 Class attributes

```python
from abc import ABC, abstractmethod

class Vehicle(ABC):

    company = "Toyota"

    @abstractmethod
    def start(self):
        pass


class Car(Vehicle):

    def start(self):
        print("Car started")


car = Car()

print(car.company)
print(Vehicle.company)
```

Output:

```text
Toyota
Toyota
```

### 4.3 Private attributes

```python
from abc import ABC, abstractmethod

class Bank(ABC):

    def __init__(self, balance):
        self.__balance = balance

    def get_balance(self):
        return self.__balance

    @abstractmethod
    def withdraw(self, amount):
        pass


class SBI(Bank):

    def withdraw(self, amount):
        print("Withdrawal processed")


account = SBI(10000)

print(account.get_balance())
```

Output:

```text
10000
```

### Attribute summary

| Attribute | Supported? |
|---|---|
| Instance attributes | Yes |
| Class attributes | Yes |
| Private attributes | Yes |
| Protected attributes | Yes |
| Properties | Yes |

---

## 5. Abstract Class with Constructor

An abstract class can have a constructor.

```python
from abc import ABC, abstractmethod

class Employee(ABC):

    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    @abstractmethod
    def calculate_bonus(self):
        pass


class Developer(Employee):

    def calculate_bonus(self):
        return self.salary * 0.20


class Manager(Employee):

    def calculate_bonus(self):
        return self.salary * 0.30


dev = Developer("Rahul", 50000)
manager = Manager("Arun", 80000)

print(dev.calculate_bonus())
print(manager.calculate_bonus())
```

Output:

```text
10000.0
24000.0
```

The parent class constructor initializes common attributes.

The child classes implement their own bonus calculation.

---

## 6. Abstract Class with Multiple Abstract Methods

An abstract class can contain multiple abstract methods.

```python
from abc import ABC, abstractmethod

class Database(ABC):

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def execute_query(self, query):
        pass

    @abstractmethod
    def disconnect(self):
        pass


class MySQL(Database):

    def connect(self):
        print("Connected to MySQL")

    def execute_query(self, query):
        print("Executing:", query)

    def disconnect(self):
        print("Disconnected")


db = MySQL()

db.connect()
db.execute_query("SELECT * FROM users")
db.disconnect()
```

Output:

```text
Connected to MySQL
Executing: SELECT * FROM users
Disconnected
```

### Important concept

What happens if a child class implements only two out of three abstract methods?

The child class also remains abstract and cannot be instantiated.

```python
class PostgreSQL(Database):

    def connect(self):
        print("Connected")

    def execute_query(self, query):
        print(query)


db = PostgreSQL()  # TypeError
```

The `disconnect()` method is missing.

---

## 7. Abstract Class with Concrete Methods

An abstract class can have both abstract and concrete methods.

```python
from abc import ABC, abstractmethod

class Vehicle(ABC):

    def start(self):
        print("Vehicle started")

    @abstractmethod
    def fuel_type(self):
        pass


class Car(Vehicle):

    def fuel_type(self):
        print("Petrol")


car = Car()

car.start()
car.fuel_type()
```

Output:

```text
Vehicle started
Petrol
```

The child class inherits the concrete method and implements the abstract method.

---

## 8. Abstract Properties

Python supports abstract properties using `@property` and `@abstractmethod`.

```python
from abc import ABC, abstractmethod

class Shape(ABC):

    @property
    @abstractmethod
    def area(self):
        pass


class Rectangle(Shape):

    def __init__(self, length, width):
        self.length = length
        self.width = width

    @property
    def area(self):
        return self.length * self.width


rectangle = Rectangle(10, 5)

print(rectangle.area)
```

Output:

```text
50
```

Every concrete subclass must provide the required property implementation.

---

## 9. Abstraction vs Encapsulation

This is a frequently asked interview question.

| Abstraction | Encapsulation |
|---|---|
| Hides implementation complexity | Bundles data and methods and controls access to state |
| Focuses on what an object does | Focuses on managing and protecting object state |
| Uses ABCs, abstract methods and contracts | Uses classes, properties and access conventions |
| Example: Payment interface | Example: Private bank balance |

### Abstraction example

```python
from abc import ABC, abstractmethod

class Payment(ABC):

    @abstractmethod
    def pay(self, amount):
        pass
```

The class defines what a payment implementation must provide.

### Encapsulation example

```python
class BankAccount:

    def __init__(self, balance):
        self.__balance = balance

    def get_balance(self):
        return self.__balance
```

The balance is managed internally through the class.

---

# ADVANCED LEVEL

## 10. Abstraction with Dependency Injection

At an advanced level, abstraction helps us build loosely coupled applications.

Example: Notification system.

Suppose an application supports:

- Email notifications.
- SMS notifications.
- WhatsApp notifications.

Instead of writing separate business logic for each notification type, define a common abstraction.

```python
from abc import ABC, abstractmethod


class NotificationService(ABC):

    @abstractmethod
    def send(self, message):
        pass


class EmailService(NotificationService):

    def send(self, message):
        print("Email:", message)


class SMSService(NotificationService):

    def send(self, message):
        print("SMS:", message)


class NotificationManager:

    def __init__(self, service):
        self.service = service

    def notify(self, message):
        self.service.send(message)


email = EmailService()
sms = SMSService()

manager1 = NotificationManager(email)
manager2 = NotificationManager(sms)

manager1.notify("Welcome!")
manager2.notify("Your OTP is 1234")
```

### Why is this important?

1. NotificationManager does not depend on a specific notification implementation.
2. We can add new notification services.
3. Existing business logic does not need modification.
4. Testing becomes easier.
5. Dependencies can be injected from outside.

This technique is called Dependency Injection.

---

## 11. Dependency Inversion Principle (DIP)

DIP is one of the SOLID principles.

Definition:

High-level modules should not depend directly on low-level modules. Both should depend on abstractions.

### Without abstraction

```python
class EmailService:

    def send(self, message):
        print("Email sent")


class NotificationManager:

    def __init__(self):
        self.email = EmailService()

    def notify(self, message):
        self.email.send(message)
```

Problem:

NotificationManager is tightly coupled to EmailService.

Replacing email with SMS requires changing the manager.

### With abstraction

```python
from abc import ABC, abstractmethod


class Notification(ABC):

    @abstractmethod
    def send(self, message):
        pass


class EmailService(Notification):

    def send(self, message):
        print("Email sent:", message)


class SMSService(Notification):

    def send(self, message):
        print("SMS sent:", message)


class NotificationManager:

    def __init__(self, service: Notification):
        self.service = service

    def notify(self, message):
        self.service.send(message)
```

Now NotificationManager depends on an abstraction rather than a concrete implementation.

---

## 12. ABC vs Protocol

Python provides another abstraction mechanism through `Protocol`.

`Protocol` supports structural typing.

```python
from typing import Protocol


class PaymentGateway(Protocol):

    def pay(self, amount: float) -> None:
        ...


class Razorpay:

    def pay(self, amount: float) -> None:
        print("Razorpay:", amount)


class Stripe:

    def pay(self, amount: float) -> None:
        print("Stripe:", amount)


def checkout(gateway: PaymentGateway):
    gateway.pay(1000)


checkout(Razorpay())
checkout(Stripe())
```

Notice that Razorpay and Stripe do not inherit from PaymentGateway.

They satisfy the contract by providing the required method.

The actual reason Protocol exists

Imagine you use 10 third-party libraries. All 10 provide a compatible pay() method, but none inherits from your PaymentGateway.
- With ABC, you need adapters or explicit inheritance to make them ABC subtypes.
- With Protocol, all 10 can satisfy the same contract without inheritance.
That's the power of structural typing.

### ABC vs Protocol

| Feature | ABC | Protocol |
|---|---|---|
| Inheritance | Normally required | Not required |
| Typing approach | Nominal typing | Structural typing |
| Runtime enforcement | Yes, for abstract methods | Not by default |
| Main purpose | Enforce class contracts | Flexible type contracts |
| Best use | Shared base behavior | Flexible APIs and dependency contracts |

**Senior-level takeaway:** Use ABC when you want a common base class and runtime enforcement. Use Protocol when you want flexible structural typing.

---

## 13. Template Method Pattern

An abstract class can define the overall workflow while child classes customize particular steps.

```python
from abc import ABC, abstractmethod


class Report(ABC):

    def generate(self):
        self.fetch_data()
        self.format_data()
        self.export()

    def fetch_data(self):
        print("Fetching data")

    @abstractmethod
    def format_data(self):
        pass

    @abstractmethod
    def export(self):
        pass


class PDFReport(Report):

    def format_data(self):
        print("Formatting PDF")

    def export(self):
        print("Exporting PDF")


report = PDFReport()
report.generate()
```

Output:

```text
Fetching data
Formatting PDF
Exporting PDF
```

This is called the Template Method Pattern.

The parent class controls the workflow, while child classes implement specific steps.

---

# SENIOR LEVEL

## 14. Real-World E-commerce Architecture

Imagine building an e-commerce application.

It needs:

| Abstract component | Possible implementations |
|---|---|
| PaymentGateway | UPI, Razorpay, Stripe |
| NotificationService | Email, SMS, WhatsApp |
| DatabaseRepository | MySQL, PostgreSQL |
| StorageService | AWS S3, Azure Blob |
| AuthenticationService | JWT, OAuth |

The business logic should depend on stable abstractions rather than implementation-specific classes.

### Benefits

1. Loose coupling.
2. Better maintainability.
3. Easier unit testing.
4. Better extensibility.
5. Easier replacement of technologies.
6. Separation of business logic from infrastructure.

## 15. When Should We Use Abstraction?

Use abstraction when:

- Multiple classes share a common contract.
- Different implementations provide the same functionality.
- You want to enforce method implementation.
- You want to reduce tight coupling.
- You want to build extensible frameworks.
- You want to make testing and maintenance easier.

Avoid unnecessary abstraction when:

- There is only one simple implementation.
- A common contract does not add value.
- It creates unnecessary complexity.
- A simple function or composition is sufficient.

## 16. Composition vs Inheritance

Senior developers should understand that inheritance is not always the best solution.

**Inheritance:** A child class inherits behavior from a parent class.

**Composition:** A class uses another object to provide functionality.

Composition is often more flexible because behavior can be replaced or injected without creating deep inheritance hierarchies.

```python
# Inheritance trap: a Stack that is-a list exposes insert(), sort(), etc. and breaks LIFO
class Stack(list): ...

# Composition: expose only what makes sense
class Stack:
    def __init__(self):
        self._items: list = []
    def push(self, x): self._items.append(x)
    def pop(self): return self._items.pop()
```
---

# INTERVIEW QUESTIONS

## Beginner-level

1. What is abstraction in Python?
2. What is an abstract class?
3. What is an abstract method?
4. What is the ABC module?
5. Can we instantiate an abstract class?
6. Can an abstract class have a constructor?
7. Can an abstract class have attributes?
8. Can an abstract class have normal methods?
9. Can an abstract class have multiple abstract methods?
10. What happens if a child class does not implement all abstract methods?

## Intermediate-level

11. What is the difference between an abstract class and a normal class?
12. Can an abstract class have private attributes?
13. Can we override an abstract method?
14. Can an abstract class contain both abstract and concrete methods?
15. What are abstract properties?
16. Can an ABC be instantiated if it has no abstract methods?
17. Can we have an abstract class without a constructor?
18. What is the difference between abstraction and encapsulation?

## Advanced-level

19. What is Dependency Injection?
20. What is the Dependency Inversion Principle?
21. How does abstraction support loose coupling?
22. What is the difference between ABC and Protocol?
23. How does abstraction improve unit testing?
24. What is the Template Method Pattern?
25. When should we use abstraction?
26. Why should we avoid unnecessary abstraction?

## Senior-level scenario questions

27. How would you design a payment system supporting multiple payment gateways?

28. How would you add a new database without changing existing business logic?

29. How would you design a notification framework supporting email, SMS and WhatsApp?

30. How would you use abstraction to mock external API dependencies during unit testing?

31. When would you choose composition over inheritance?

32. How would you prevent an abstract base class from becoming too large?

---

# PRACTICAL CODING EXERCISES

### Level 1 – Beginner

Create an abstract class Vehicle.

Requirements:
- Abstract method: start()
- Implement Bike, Car and Bus.
- Each class should provide its own start() implementation.

### Level 2 – Intermediate

Create an abstract class Bank.

Requirements:
- deposit()
- withdraw()
- check_balance()

Implement SBI and HDFC with their own withdrawal rules.

### Level 3 – Advanced

Create an abstract PaymentGateway.

Implement:
- UPI
- CreditCard
- NetBanking

Use dependency injection to select the payment method dynamically.

### Level 4 – Senior

Design an e-commerce payment architecture.

Requirements:
- Multiple payment gateways.
- Payment validation.
- Refund functionality.
- Logging.
- Exception handling.
- Unit testing using mocks.
- Adding a new gateway should not require changing core business logic.

---

# QUICK REVISION NOTES

| Concept | Remember |
|---|---|
| ABC | Abstract Base Class |
| abstractmethod | Defines mandatory abstract methods |
| Abstract class | Defines a common structure and contract |
| Concrete class | Implements required abstract methods |
| Constructor | Allowed in abstract classes |
| Attributes | Allowed in abstract classes |
| Concrete methods | Allowed in abstract classes |
| Object creation | Not allowed while abstract methods remain unimplemented |
| Protocol | Supports structural typing |
| Dependency Injection | Supplies dependencies from outside |
| DIP | High-level modules depend on abstractions |
| Template Method | Parent controls workflow; children customize steps |

## Final Interview Definition

"Abstraction is an OOP principle that hides implementation details and exposes essential functionality. In Python, we commonly implement abstraction using the abc module, ABC and abstractmethod. An abstract class defines a contract that concrete subclasses must implement. It can also contain constructors, attributes and concrete methods. Abstraction helps us achieve loose coupling, maintainability, extensibility and better software architecture."

**Learning advice:** Master the first nine sections before moving to SOLID principles, design patterns, dependency injection and system design. This gives you a strong foundation for Python developer interviews from junior to senior level.