
from functools import wraps

user_permissions = ["view_user", "edit_user"]

# Parameterized implementaion
def authorize_permissions(*args, **kwargs):

    permissions = kwargs.get("permissions", [])

    def _authorize_permissions(func):

        @wraps(func)
        def wrapper(*func_args, **func_kwargs):

            has_permission = all(
                permission in user_permissions
                for permission in permissions
            )

            if has_permission:
                return func(*func_args, **func_kwargs)

            raise Exception("Unauthorized")

        return wrapper

    return _authorize_permissions


@authorize_permissions(permissions=["view_user"])
def greet(name, age):
    return f"Hello {name}, your age is {age}"


print(greet("Swaroopa", age=10))

# -------property decorator


class Test:

    def __init__(self):
        self._value = 10

    @property
    def value(self):
        print("Getter called")
        return self._value

    @value.setter
    def value(self, val):
        print("Setter called")
        self._value = val


obj = Test()

obj.value = 20

print(obj.value)