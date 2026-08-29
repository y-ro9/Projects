#!/usr/bin/env python3
"""
Password Strength Analyzer - Cybersecurity Project
Author: YASH RAJ
Date: 18-08-2026
"""

import re
import math
import hashlib
import requests
import string
import random
from typing import Dict, List

class PasswordStrengthAnalyzer:
    """Main class for password strength analysis"""
    
    def __init__(self):
        self.special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        # Combined banned words from both your codes
        self.banned_words = {
            # Common passwords
            "123456", "password", "qwerty", "abc123", "admin", 
            "letmein", "welcome", "guest", "student",
            # Common names
            "john", "robert", "michael", "james", "mary", 
            "rahul", "priya", "amit", "sneha", "raj",
            # Common cities
            "india", "delhi", "mumbai", "bangalore"
        }
        
        # Keyboard patterns
        self.keyboard_patterns = ["qwerty", "asdf", "zxcv", "qazwsx"]
        
        # Load leaked passwords
        self.leaked_passwords = self._load_leaked()
    
    def _load_leaked(self) -> set:
        """Load leaked passwords"""
        try:
            with open('leaked.txt', 'r') as f:
                return set(line.strip().lower() for line in f)
        except:
            return {"password", "123456", "qwerty", "admin", "letmein"}
    
    def analyze(self, password: str) -> Dict:
        """Main analysis function"""
        results = {
            'password': password,
            'score': 0,
            'entropy': 0,
            'strength': '',
            'issues': [],
            'suggestions': []
        }
        
        # Check 1: Length
        if len(password) < 8:
            results['issues'].append('Minimum 8 characters required')
        
        # Check 2: Character types
        checks = {
            'uppercase': any(c.isupper() for c in password),
            'lowercase': any(c.islower() for c in password),
            'digit': any(c.isdigit() for c in password),
            'special': any(c in self.special_chars for c in password)
        }
        
        for check, passed in checks.items():
            if not passed:
                results['issues'].append(f'Missing {check} character')
        
        # Check 3: Patterns 
        if self._has_sequential(password):
            results['issues'].append('Contains sequential pattern (123/abc)')
        
        if self._has_repeats(password):
            results['issues'].append('Contains repeated characters (aaa/111)')
        
        # Check 4: Common patterns
        if self._has_keyboard_pattern(password):
            results['issues'].append('Contains keyboard pattern (qwerty)')
        
        if self._has_common_word(password):
            results['issues'].append('Contains common word/name')
        
        if self._has_date(password):
            results['issues'].append('Contains year/date')
        
        # Check 5: Leaked
        if password.lower() in self.leaked_passwords:
            results['issues'].append('Password is leaked!')
        
        # Calculate entropy
        results['entropy'] = self._calculate_entropy(password)
        
        # Calculate score
        results['score'] = self._calculate_score(results, checks)
        
        # Determine strength
        if results['score'] >= 80:
            results['strength'] = 'Strong 💪'
        elif results['score'] >= 60:
            results['strength'] = 'Good 👍'
        elif results['score'] >= 40:
            results['strength'] = 'Weak ⚠️'
        else:
            results['strength'] = 'Very Weak ❌'
        
        # Generate suggestions
        results['suggestions'] = self._get_suggestions(results)
        
        return results
    
    def _has_sequential(self, password: str) -> bool:
        """Check for 123, abc, 321, cba patterns"""
        lower = password.lower()
        for i in range(len(password) - 2):
            # Forward sequence
            if (ord(lower[i]) + 1 == ord(lower[i+1]) and 
                ord(lower[i+1]) + 1 == ord(lower[i+2])):
                return True
            # Reverse sequence
            if (ord(lower[i]) - 1 == ord(lower[i+1]) and 
                ord(lower[i+1]) - 1 == ord(lower[i+2])):
                return True
        return False
    
    def _has_repeats(self, password: str) -> bool:
        """Check for aaa, 111 patterns"""
        for i in range(len(password) - 2):
            if password[i] == password[i+1] == password[i+2]:
                return True
        return False
    
    def _has_keyboard_pattern(self, password: str) -> bool:
        """Check for keyboard patterns"""
        lower = password.lower()
        return any(pattern in lower for pattern in self.keyboard_patterns)
    
    def _has_common_word(self, password: str) -> bool:
        """Check for common words/names"""
        lower = password.lower()
        return any(word in lower for word in self.banned_words)
    
    def _has_date(self, password: str) -> bool:
        """Check for dates/years"""
        if re.search(r'(19|20)\d{2}', password):
            return True
        if re.search(r'\d{2}[/\-.]?\d{2}[/\-.]?\d{4}', password):
            return True
        return False
    
    def _calculate_entropy(self, password: str) -> float:
        """Calculate password entropy"""
        pool = 0
        if any(c.islower() for c in password): pool += 26
        if any(c.isupper() for c in password): pool += 26
        if any(c.isdigit() for c in password): pool += 10
        if any(c in self.special_chars for c in password): pool += len(self.special_chars)
        
        if pool == 0:
            return 0
        
        return round(len(password) * math.log2(pool), 2)
    
    def _calculate_score(self, results: Dict, checks: Dict) -> int:
        """Calculate final score"""
        score = 0
        
        # Length (max 20 points)
        if len(results['password']) >= 12:
            score += 20
        elif len(results['password']) >= 8:
            score += 10
        
        # Character types (max 20 points)
        score += sum(checks.values()) * 5
        
        # No issues (max 30 points)
        issues_count = len(results['issues'])
        score += max(0, 30 - (issues_count * 5))
        
        # Entropy bonus (max 30 points)
        entropy = results['entropy']
        if entropy >= 60:
            score += 30
        elif entropy >= 40:
            score += 20
        elif entropy >= 25:
            score += 10
        
        return min(100, score)
    
    def _get_suggestions(self, results: Dict) -> List[str]:
        """Generate suggestions"""
        suggestions = []
        password = results['password']
        
        if len(password) < 12:
            suggestions.append("Make it 12+ characters long")
        
        if not any(c.isupper() for c in password):
            suggestions.append("Add uppercase letters")
        if not any(c.islower() for c in password):
            suggestions.append("Add lowercase letters")
        if not any(c.isdigit() for c in password):
            suggestions.append("Add numbers")
        if not any(c in self.special_chars for c in password):
            suggestions.append("Add special characters (!@#$%^&*)")
        
        if self._has_sequential(password):
            suggestions.append("Avoid sequences like 123 or abc")
        if self._has_repeats(password):
            suggestions.append("Avoid repeated characters")
        if self._has_keyboard_pattern(password):
            suggestions.append("Avoid keyboard patterns")
        if self._has_common_word(password):
            suggestions.append("Avoid common words/names")
        if self._has_date(password):
            suggestions.append("Avoid dates/years")
        
        return suggestions[:4]
    
    def generate_password(self, length: int = 16) -> str:
        """Generate strong password"""
        chars = string.ascii_letters + string.digits + self.special_chars
        
        # Ensure all types
        password = [
            random.choice(string.ascii_lowercase),
            random.choice(string.ascii_uppercase),
            random.choice(string.digits),
            random.choice(self.special_chars)
        ]
        
        password.extend(random.choice(chars) for _ in range(length - 4))
        random.shuffle(password)
        password = ''.join(password)
        
        # Verify it passes checks
        results = self.analyze(password)
        if results['score'] >= 70:
            return password
        else:
            return self.generate_password(length)

def main():
    """Main program"""
    analyzer = PasswordStrengthAnalyzer()
    
    print("\n" + "="*50)
    print("🔐 PASSWORD STRENGTH ANALYZER")
    print("="*50)
    
    while True:
        print("\n1. Check Password")
        print("2. Generate Password")
        print("3. Exit")
        
        choice = input("\nSelect (1-3): ").strip()
        
        if choice == '1':
            pwd = input("Enter password: ").strip()
            if not pwd:
                continue
            
            result = analyzer.analyze(pwd)
            
            print("\n" + "-"*40)
            print(f"Password: {'*' * len(pwd)}")
            print(f"Strength: {result['strength']} ({result['score']}/100)")
            print(f"Entropy: {result['entropy']} bits")
            
            if result['issues']:
                print("\n⚠️ Issues:")
                for issue in result['issues']:
                    print(f"  • {issue}")
            
            if result['suggestions']:
                print("\n💡 Suggestions:")
                for suggestion in result['suggestions']:
                    print(f"  • {suggestion}")
            print("-"*40)
            
        elif choice == '2':
            try:
                length = int(input("Length (default 16): ") or 16)
                if length < 8:
                    length = 8
                
                pwd = analyzer.generate_password(length)
                result = analyzer.analyze(pwd)
                
                print(f"\n✅ Generated: {pwd}")
                print(f"Strength: {result['strength']} ({result['score']}/100)")
                print(f"Entropy: {result['entropy']} bits")
                
            except ValueError:
                print("❌ Enter a valid number")
            
        elif choice == '3':
            print("\n👋 Stay Secure!")
            break
        
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    main()