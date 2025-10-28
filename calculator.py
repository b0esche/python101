def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b != 0:
        return a / b
    else:
        return "Cannot divide by zero"

# Example usage
print("Simple Calculator")
print("Addition: 5 + 3 =", add(5, 3))
print("Subtraction: 5 - 3 =", subtract(5, 3))
print("Multiplication: 5 * 3 =", multiply(5, 3))
print("Division: 5 / 3 =", divide(5, 3))