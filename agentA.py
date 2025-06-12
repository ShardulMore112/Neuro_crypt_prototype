import random

class EncoderAgentA:
    def __init__(self):
        self.rules = {
            'vowel_to_digit': self.vowel_to_digit,
            'ascii_shift': self.ascii_shift,
            'reverse_text': self.reverse_text,
            'mask_consonants': self.mask_consonants,
            'leetspeak': self.leetspeak,
            'fibonacci_cipher': self.fibonacci_cipher  # New unknown rule
        }

    def vowel_to_digit(self, text):
        mapping = {'a': '1', 'e': '2', 'i': '3', 'o': '4', 'u': '5'}
        return ''.join([mapping.get(c.lower(), c) for c in text])

    def ascii_shift(self, text):
        shift = random.choice([-1, 1, 2])
        return ''.join([chr((ord(c)+shift) % 256) if c.isalpha() else c for c in text])

    def reverse_text(self, text):
        return text[::-1]

    def mask_consonants(self, text):
        vowels = 'aeiouAEIOU'
        return ''.join([c if c in vowels else '#' for c in text])

    def leetspeak(self, text):
        mapping = {'a': '@', 'e': '3', 'i': '1', 'o': '0', 't': '7'}
        return ''.join([mapping.get(c.lower(), c) for c in text])

    def fibonacci_cipher(self, text):
        # Replace each char with the ith Fibonacci number mod 26 as a character (a-z)
        fib = [0, 1]
        while len(fib) < len(text):
            fib.append(fib[-1] + fib[-2])
        return ''.join([chr(97 + (fib[i] % 26)) for i in range(len(text))])

    def encode(self, text, rule_name=None):
        if rule_name is None:
            rule_name = random.choice(list(self.rules.keys()))
        rule_func = self.rules[rule_name]
        encoded = rule_func(text)
        return {
            'plain': text,
            'encoded': encoded,
            'rule_name': rule_name
        }

    def generate_dataset(self, samples=10, words=None, include_rules=None):
        if not words:
            words = ['hello', 'world', 'openai', 'neural', 'cipher', 'matrix', 'reward', 'agent', 'encode', 'brain']
        dataset = []
        for _ in range(samples):
            word = random.choice(words)
            if include_rules:
                rule = random.choice(include_rules)
            else:
                rule = None
            data = self.encode(word, rule)
            dataset.append(data)
        return dataset




if __name__ == "__main__":
    agent = EncoderAgentA()

    print("🔐 Mixed Rule Dataset:")
    mixed_data = agent.generate_dataset(samples=5)
    for entry in mixed_data:
        print(f"Plain: {entry['plain']}\tEncoded: {entry['encoded']}\t(Rule: {entry['rule_name']})")

    print("\n🧠 Unfamiliar Rule Only (Fibonacci):")
    fib_data = agent.generate_dataset(samples=5, include_rules=['fibonacci_cipher'])
    for entry in fib_data:
        print(f"Plain: {entry['plain']}\tEncoded: {entry['encoded']}\t(Rule: {entry['rule_name']})")
