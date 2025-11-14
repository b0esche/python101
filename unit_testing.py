import unittest
import math
from typing import List

class Calculator:
    def add(self, a: float, b: float) -> float:
        return a + b
    
    def subtract(self, a: float, b: float) -> float:
        return a - b
    
    def multiply(self, a: float, b: float) -> float:
        return a * b
    
    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
    
    def power(self, base: float, exponent: float) -> float:
        return base ** exponent
    
    def sqrt(self, x: float) -> float:
        if x < 0:
            raise ValueError("Cannot calculate square root of negative number")
        return math.sqrt(x)

class TextProcessor:
    def reverse_string(self, text: str) -> str:
        return text[::-1]
    
    def count_words(self, text: str) -> int:
        if not text.strip():
            return 0
        return len(text.split())
    
    def capitalize_words(self, text: str) -> str:
        return ' '.join(word.capitalize() for word in text.split())
    
    def is_palindrome(self, text: str) -> bool:
        cleaned = ''.join(c.lower() for c in text if c.isalnum())
        return cleaned == cleaned[::-1]
    
    def remove_duplicates(self, text: str) -> str:
        seen = set()
        result = []
        for char in text:
            if char not in seen:
                seen.add(char)
                result.append(char)
        return ''.join(result)

class DataValidator:
    def is_email_valid(self, email: str) -> bool:
        if '@' not in email or email.count('@') != 1:
            return False
        
        local, domain = email.split('@')
        
        if not local or not domain:
            return False
        
        if '.' not in domain:
            return False
        
        return True
    
    def is_phone_valid(self, phone: str) -> bool:
        digits = ''.join(c for c in phone if c.isdigit())
        return len(digits) >= 10
    
    def is_url_valid(self, url: str) -> bool:
        return url.startswith(('http://', 'https://', 'www.'))

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()
    
    def test_add(self):
        self.assertEqual(self.calc.add(2, 3), 5)
        self.assertEqual(self.calc.add(-1, 1), 0)
        self.assertEqual(self.calc.add(0, 0), 0)
    
    def test_subtract(self):
        self.assertEqual(self.calc.subtract(5, 3), 2)
        self.assertEqual(self.calc.subtract(1, 1), 0)
        self.assertEqual(self.calc.subtract(-1, -1), 0)
    
    def test_multiply(self):
        self.assertEqual(self.calc.multiply(3, 4), 12)
        self.assertEqual(self.calc.multiply(0, 5), 0)
        self.assertEqual(self.calc.multiply(-2, 3), -6)
    
    def test_divide(self):
        self.assertEqual(self.calc.divide(10, 2), 5)
        self.assertEqual(self.calc.divide(-6, 3), -2)
        
        with self.assertRaises(ValueError):
            self.calc.divide(5, 0)
    
    def test_power(self):
        self.assertEqual(self.calc.power(2, 3), 8)
        self.assertEqual(self.calc.power(5, 0), 1)
        self.assertEqual(self.calc.power(0, 5), 0)
    
    def test_sqrt(self):
        self.assertEqual(self.calc.sqrt(9), 3)
        self.assertEqual(self.calc.sqrt(0), 0)
        
        with self.assertRaises(ValueError):
            self.calc.sqrt(-1)

class TestTextProcessor(unittest.TestCase):
    def setUp(self):
        self.text = TextProcessor()
    
    def test_reverse_string(self):
        self.assertEqual(self.text.reverse_string("hello"), "olleh")
        self.assertEqual(self.text.reverse_string(""), "")
        self.assertEqual(self.text.reverse_string("a"), "a")
    
    def test_count_words(self):
        self.assertEqual(self.text.count_words("hello world"), 2)
        self.assertEqual(self.text.count_words("   "), 0)
        self.assertEqual(self.text.count_words(""), 0)
        self.assertEqual(self.text.count_words("one"), 1)
    
    def test_capitalize_words(self):
        self.assertEqual(self.text.capitalize_words("hello world"), "Hello World")
        self.assertEqual(self.text.capitalize_words("PYTHON programming"), "Python Programming")
        self.assertEqual(self.text.capitalize_words(""), "")
    
    def test_is_palindrome(self):
        self.assertTrue(self.text.is_palindrome("racecar"))
        self.assertTrue(self.text.is_palindrome("A man a plan a canal Panama"))
        self.assertFalse(self.text.is_palindrome("hello"))
        self.assertTrue(self.text.is_palindrome(""))
    
    def test_remove_duplicates(self):
        self.assertEqual(self.text.remove_duplicates("hello"), "helo")
        self.assertEqual(self.text.remove_duplicates("aaaa"), "a")
        self.assertEqual(self.text.remove_duplicates(""), "")

class TestDataValidator(unittest.TestCase):
    def setUp(self):
        self.validator = DataValidator()
    
    def test_is_email_valid(self):
        self.assertTrue(self.validator.is_email_valid("test@example.com"))
        self.assertTrue(self.validator.is_email_valid("user.name@domain.co.uk"))
        
        self.assertFalse(self.validator.is_email_valid("invalid-email"))
        self.assertFalse(self.validator.is_email_valid("@domain.com"))
        self.assertFalse(self.validator.is_email_valid("user@"))
        self.assertFalse(self.validator.is_email_valid("user@@domain.com"))
    
    def test_is_phone_valid(self):
        self.assertTrue(self.validator.is_phone_valid("123-456-7890"))
        self.assertTrue(self.validator.is_phone_valid("(123) 456-7890"))
        self.assertTrue(self.validator.is_phone_valid("1234567890"))
        
        self.assertFalse(self.validator.is_phone_valid("123-456"))
        self.assertFalse(self.validator.is_phone_valid("abc-def-ghij"))
    
    def test_is_url_valid(self):
        self.assertTrue(self.validator.is_url_valid("https://www.example.com"))
        self.assertTrue(self.validator.is_url_valid("http://example.com"))
        self.assertTrue(self.validator.is_url_valid("www.example.com"))
        
        self.assertFalse(self.validator.is_url_valid("example.com"))
        self.assertFalse(self.validator.is_url_valid("not-a-url"))

class TestIntegration(unittest.TestCase):
    def test_calculator_text_integration(self):
        calc = Calculator()
        text = TextProcessor()
        
        result = calc.add(2, 3)
        text_result = text.reverse_string(str(result))
        
        self.assertEqual(text_result, "5")
    
    def test_validator_text_integration(self):
        validator = DataValidator()
        text = TextProcessor()
        
        email = "test@example.com"
        is_valid = validator.is_email_valid(email)
        reversed_email = text.reverse_string(email)
        
        self.assertTrue(is_valid)
        self.assertEqual(reversed_email, "moc.elpmaxe@tset")

def run_performance_test():
    import time
    
    calc = Calculator()
    text = TextProcessor()
    
    print("\nPerformance Tests:")
    print("=" * 30)
    
    start_time = time.time()
    for i in range(10000):
        calc.add(i, i+1)
    add_time = time.time() - start_time
    print(f"10,000 additions: {add_time:.4f} seconds")
    
    start_time = time.time()
    for i in range(1000):
        text.reverse_string("hello world " * 10)
    reverse_time = time.time() - start_time
    print(f"1,000 string reversals: {reverse_time:.4f} seconds")

def create_test_suite():
    suite = unittest.TestSuite()
    
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestCalculator))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestTextProcessor))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestDataValidator))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestIntegration))
    
    return suite

def main():
    print("Unit Testing Examples")
    print("=" * 50)
    
    print("\n1. Running individual test classes:")
    print("\nCalculator Tests:")
    unittest.main(argv=[''], exit=False, defaultTest='TestCalculator')
    
    print("\n2. Running custom test suite:")
    suite = create_test_suite()
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print(f"\nTests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\nFailures:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\nErrors:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    run_performance_test()
    
    print("\n3. Test coverage example:")
    print("To get test coverage, install coverage package:")
    print("pip install coverage")
    print("coverage run -m unittest test_module.py")
    print("coverage report")
    print("coverage html")

if __name__ == "__main__":
    main()