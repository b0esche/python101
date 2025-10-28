# Basic data analysis with lists and dictionaries

# Sample data
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
student_grades = {"Alice": 85, "Bob": 92, "Charlie": 78, "Diana": 96}

# List operations
print("Numbers:", numbers)
print("Sum:", sum(numbers))
print("Average:", sum(numbers) / len(numbers))
print("Max:", max(numbers))
print("Min:", min(numbers))

# Dictionary operations
print("\nStudent Grades:")
for student, grade in student_grades.items():
    print(f"{student}: {grade}")

print("Highest grade:", max(student_grades.values()))
print("Average grade:", sum(student_grades.values()) / len(student_grades))