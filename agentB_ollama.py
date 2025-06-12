import subprocess
import json
import re
import os
import csv
from datetime import datetime

class DecoderAgentB:
    def __init__(self, model_name="llama3", memory_file="examples_memory.json", log_file="decode_log.csv"):
        self.model_name = model_name
        self.memory_file = memory_file
        self.log_file = log_file
        self.examples = self.load_memory()

        # Initialize log file if not present
        if not os.path.exists(self.log_file):
            with open(self.log_file, mode='w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Timestamp", "Encoded", "Predicted", "Actual", "Score", "Rule"])

    def load_memory(self):
        if os.path.exists(self.memory_file):
            with open(self.memory_file, 'r') as f:
                return json.load(f)
        return []

    def save_memory(self):
        with open(self.memory_file, 'w') as f:
            json.dump(self.examples, f)

    def log_prediction(self, encoded, predicted, actual, score, rule="unknown"):
        with open(self.log_file, mode='a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([datetime.now().isoformat(), encoded, predicted, actual, round(score, 2), rule])

    def decode(self, new_example, target):
        self.examples.append(new_example)
        self.examples = sorted(self.examples, key=lambda x: x.get('score', 0), reverse=True)[:10]  # keep top 10
        self.save_memory()

        # Filter examples by same rule
        rule = new_example.get("rule", "")
        relevant_examples = [ex for ex in self.examples if ex.get("rule") == rule]
        if not relevant_examples:
            relevant_examples = self.examples[:3]  # fallback to top 3 examples

        # Prepare prompt
        prompt = (
            "You are a decoding AI. Given encoded words and decoding rules, respond with the final decoded word.\n"
            "Only respond with the single decoded word. Do NOT explain or use punctuation.\n"
        )
        for i, ex in enumerate(relevant_examples):
            prompt += f"Example {i+1} (Rule: {ex['rule']}):\nEncoded: {ex['encoded']}\nPlain: {ex['plain']}\n\n"
        prompt += f"New Encrypted Word (Rule: {rule}): {target}\nPlain:"

        try:
            result = subprocess.run(
                ["ollama", "run", self.model_name],
                input=prompt,
                text=True,
                capture_output=True,
                encoding='utf-8',
                timeout=15
            )
            output = result.stdout.strip()
            match = re.search(r"\b[a-zA-Z]{3,12}\b", output)
            if match:
                return match.group(0).lower()
            else:
                print(f"⚠️ Could not parse output: {output}")
                return "error"

        except subprocess.TimeoutExpired:
            print("⏱️ Ollama model timed out.")
            return "error"
        except Exception as e:
            print(f"❌ Ollama error: {e}")
            return "error"

    def auto_tuned_decode(self, new_example, target, actual_plain, evaluator, base_delay=1, max_retries=3):
        import time
        delay = base_delay
        for attempt in range(max_retries):
            prediction = self.decode(new_example, target)
            if prediction == "error":
                print(f"⏳ Retry {attempt + 1} after {delay} seconds...")
                time.sleep(delay)
                delay *= 2
            else:
                feedback = evaluator.give_feedback(prediction, actual_plain)
                new_example['score'] = feedback['score']
                self.log_prediction(target, prediction, actual_plain, feedback['score'], new_example.get("rule", ""))
                return prediction, feedback

        self.log_prediction(target, "error", actual_plain, 0.0, new_example.get("rule", ""))
        return "error", {'score': 0.0, 'feedback': "Failed to decode after retries"}
