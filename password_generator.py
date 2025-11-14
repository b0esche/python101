import random
import string
import secrets
import hashlib
import base64
from typing import List, Optional

class PasswordGenerator:
    def __init__(self):
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        self.ambiguous = "il1Lo0O"
    
    def generate_password(self, 
                         length: int = 12,
                         include_uppercase: bool = True,
                         include_lowercase: bool = True,
                         include_digits: bool = True,
                         include_symbols: bool = True,
                         exclude_ambiguous: bool = False,
                         no_repeating: bool = False) -> str:
        
        if length < 4:
            raise ValueError("Password length must be at least 4 characters")
        
        charset = ""
        required_chars = []
        
        if include_lowercase:
            charset += self.lowercase
            required_chars.append(random.choice(self.lowercase))
        
        if include_uppercase:
            charset += self.uppercase
            required_chars.append(random.choice(self.uppercase))
        
        if include_digits:
            charset += self.digits
            required_chars.append(random.choice(self.digits))
        
        if include_symbols:
            charset += self.symbols
            required_chars.append(random.choice(self.symbols))
        
        if exclude_ambiguous:
            charset = ''.join(c for c in charset if c not in self.ambiguous)
        
        if not charset:
            raise ValueError("No character sets selected")
        
        remaining_length = length - len(required_chars)
        
        if no_repeating:
            available_chars = list(charset)
            random.shuffle(available_chars)
            
            if len(available_chars) < remaining_length:
                raise ValueError("Not enough unique characters for password with no repeats")
            
            additional_chars = random.sample(available_chars, remaining_length)
        else:
            additional_chars = [random.choice(charset) for _ in range(remaining_length)]
        
        password_chars = required_chars + additional_chars
        random.shuffle(password_chars)
        
        return ''.join(password_chars)
    
    def generate_secure_password(self, length: int = 16) -> str:
        alphabet = string.ascii_letters + string.digits + self.symbols
        return ''.join(secrets.choice(alphabet) for _ in range(length))
    
    def generate_passphrase(self, 
                           word_count: int = 4,
                           separator: str = "-",
                           capitalize: bool = False,
                           include_numbers: bool = False) -> str:
        
        word_list = [
            "apple", "banana", "coffee", "dragon", "elephant", "forest", "guitar", "hammer",
            "island", "jungle", "kitten", "lemon", "mountain", "ocean", "penguin", "queen",
            "rabbit", "sunset", "tiger", "umbrella", "village", "window", "yellow", "zebra",
            "butterfly", "chocolate", "diamond", "fireworks", "galaxy", "happiness", "rainbow",
            "thunder", "volcano", "adventure", "blossom", "crystal", "discovery", "enchantment",
            "fascination", "glimmer", "harmony", "inspiration", "journey", "luminous", "mystery",
            "nebula", "paradise", "quasar", "serenity", "twilight", "universe", "whisper",
            "xylophone", "yesterday", "zenith"
        ]
        
        words = random.choices(word_list, k=word_count)
        
        if capitalize:
            words = [word.capitalize() for word in words]
        
        if include_numbers:
            words = [f"{word}{random.randint(0, 99)}" for word in words]
        
        return separator.join(words)
    
    def check_password_strength(self, password: str) -> dict:
        score = 0
        feedback = []
        
        if len(password) >= 8:
            score += 1
        else:
            feedback.append("Password should be at least 8 characters long")
        
        if len(password) >= 12:
            score += 1
        
        if len(password) >= 16:
            score += 1
        
        if any(c.islower() for c in password):
            score += 1
        else:
            feedback.append("Include lowercase letters")
        
        if any(c.isupper() for c in password):
            score += 1
        else:
            feedback.append("Include uppercase letters")
        
        if any(c.isdigit() for c in password):
            score += 1
        else:
            feedback.append("Include numbers")
        
        if any(c in self.symbols for c in password):
            score += 1
        else:
            feedback.append("Include special characters")
        
        if not any(c in self.ambiguous for c in password):
            score += 1
        
        strength_levels = {
            0: "Very Weak",
            1: "Weak",
            2: "Fair",
            3: "Good",
            4: "Strong",
            5: "Very Strong",
            6: "Excellent",
            7: "Maximum"
        }
        
        return {
            "score": score,
            "max_score": 7,
            "strength": strength_levels.get(score, "Unknown"),
            "feedback": feedback
        }
    
    def hash_password(self, password: str, salt: Optional[str] = None) -> tuple:
        if salt is None:
            salt = secrets.token_hex(16)
        
        password_hash = hashlib.pbkdf2_hmac('sha256', 
                                          password.encode('utf-8'), 
                                          salt.encode('utf-8'), 
                                          100000)
        
        return base64.b64encode(password_hash).decode('utf-8'), salt
    
    def verify_password(self, password: str, stored_hash: str, salt: str) -> bool:
        computed_hash, _ = self.hash_password(password, salt)
        return computed_hash == stored_hash

def main():
    generator = PasswordGenerator()
    
    print("Password Generator Examples")
    print("=" * 50)
    
    print("\n1. Basic password generation:")
    for i in range(3):
        password = generator.generate_password(12)
        print(f"Password {i+1}: {password}")
    
    print("\n2. Secure password generation:")
    for i in range(3):
        password = generator.generate_secure_password(16)
        print(f"Secure {i+1}: {password}")
    
    print("\n3. Custom password generation:")
    password = generator.generate_password(
        length=14,
        include_symbols=True,
        exclude_ambiguous=True,
        no_repeating=True
    )
    print(f"Custom: {password}")
    
    print("\n4. Passphrase generation:")
    for i in range(3):
        passphrase = generator.generate_passphrase(
            word_count=4,
            separator=" ",
            capitalize=True,
            include_numbers=True
        )
        print(f"Passphrase {i+1}: {passphrase}")
    
    print("\n5. Password strength analysis:")
    test_passwords = [
        "password",
        "Password123",
        "P@ssw0rd!",
        "MySecureP@ssword2024!",
        generator.generate_secure_password(16)
    ]
    
    for pwd in test_passwords:
        strength = generator.check_password_strength(pwd)
        print(f"\nPassword: {pwd}")
        print(f"Strength: {strength['strength']} ({strength['score']}/{strength['max_score']})")
        if strength['feedback']:
            print("Feedback:", ", ".join(strength['feedback']))
    
    print("\n6. Password hashing:")
    password = "MySecurePassword123!"
    hashed, salt = generator.hash_password(password)
    print(f"Original: {password}")
    print(f"Hashed: {hashed}")
    print(f"Salt: {salt}")
    
    verified = generator.verify_password("MySecurePassword123!", hashed, salt)
    print(f"Verification (correct): {verified}")
    
    verified_wrong = generator.verify_password("WrongPassword", hashed, salt)
    print(f"Verification (wrong): {verified_wrong}")

if __name__ == "__main__":
    main()