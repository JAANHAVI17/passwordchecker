import re
import random
import string
from enum import Enum, auto

class PasswordStrength(Enum):
    WEAK = auto()
    MEDIUM = auto()
    STRONG = auto()
    VERY_STRONG = auto()

class PasswordChecker:
    @staticmethod
    def check_strength(password):
        """Check password strength with detailed rules"""
        if not password:
            return PasswordStrength.WEAK, {}
            
        checks = {
            "Length ≥ 12 chars": len(password) >= 12,
            "Length ≥ 8 chars": len(password) >= 8,
            "Uppercase Letter": re.search(r'[A-Z]', password) is not None,
            "Lowercase Letter": re.search(r'[a-z]', password) is not None,
            "Digit": re.search(r'[0-9]', password) is not None,
            "Special Character": re.search(r'[!@#$%^&*(),.?":{}|<>]', password) is not None,
            "No Common Pattern": not any(
                common in password.lower() 
                for common in ["password", "123", "qwerty", "admin", "welcome"]
            ),
            "No Repeating Chars": not re.search(r'(.)\1{2,}', password),
            "No Sequential Chars": not any(
                all(c in password.lower() for c in seq)
                for seq in ["abc", "123", "qwe", "asd"]
            )
        }
        
        passed = sum(checks.values())
        total = len(checks)
        
        if passed == total:
            strength = PasswordStrength.VERY_STRONG
        elif passed >= total - 2:
            strength = PasswordStrength.STRONG
        elif passed >= total // 2:
            strength = PasswordStrength.MEDIUM
        else:
            strength = PasswordStrength.WEAK
            
        return strength, checks

    @staticmethod
    def generate_strong_password(length=16):
        """Generate a random strong password with guaranteed complexity"""
        lower = string.ascii_lowercase
        upper = string.ascii_uppercase
        digits = string.digits
        special = "!@#$%^&*()"
        
        # Ensure at least one of each character type
        password = [
            random.choice(lower),
            random.choice(upper),
            random.choice(digits),
            random.choice(special)
        ]
        
        # Fill the rest randomly
        all_chars = lower + upper + digits + special
        password.extend(random.choice(all_chars) for _ in range(length - 4))
        
        # Shuffle and return as string
        random.shuffle(password)
        return ''.join(password)