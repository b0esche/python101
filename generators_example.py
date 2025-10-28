def fibonacci_generator(n):
    a, b = 0, 1
    count = 0
    while count < n:
        yield a
        a, b = b, a + b
        count += 1

def even_numbers(limit):
    num = 0
    while num <= limit:
        yield num
        num += 2

# Example usage
print("Fibonacci sequence:")
for num in fibonacci_generator(10):
    print(num, end=" ")
print()

print("Even numbers up to 20:")
for num in even_numbers(20):
    print(num, end=" ")
print()