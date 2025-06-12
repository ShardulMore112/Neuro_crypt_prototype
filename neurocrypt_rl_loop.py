import json
import os
from agentA import EncoderAgentA
from agentB import DecoderAgentB
from feedback import FeedbackEvaluator

# 📦 File to persist examples between runs
EXAMPLE_MEMORY_FILE = "learned_examples.json"

# 🧠 Load previous few-shot examples
def load_examples():
    if os.path.exists(EXAMPLE_MEMORY_FILE):
        with open(EXAMPLE_MEMORY_FILE, "r") as f:
            return json.load(f)
    return []

# 💾 Save updated examples
def save_examples(examples):
    with open(EXAMPLE_MEMORY_FILE, "w") as f:
        json.dump(examples, f, indent=2)

# 🧠 Initialize components
encoder = EncoderAgentA()
decoder = DecoderAgentB(groq_api_key="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")  # replace with your key
evaluator = FeedbackEvaluator()

# 🧪 Generate new test dataset
dataset = encoder.generate_dataset(samples=20)

# 📥 Load memory of past successful or failed examples
examples = load_examples()
eval_history = []

print("\n🔁 NeuroCrypt-RL Feedback Loop Running...\n")

for i, sample in enumerate(dataset):
    print(f"[{i+1}] Plain: {sample['plain']} | Encoded: {sample['encoded']} | Rule: {sample['rule_name']}")

    # Run Decoder (Agent B)
    prediction = decoder.decode(examples, sample['encoded'])

    # Evaluate performance
    feedback = evaluator.give_feedback(prediction, sample['plain'])
    eval_history.append(feedback["score"])

    print(f"🔍 Predicted: {prediction} | Feedback: {feedback['feedback']}\n")

    # 🧠 Learn from incorrect attempts (Reinforcement update)
    if feedback["score"] < 1.0:
        examples.append({"encoded": sample["encoded"], "plain": sample["plain"]})

# 💾 Save updated examples back to memory
save_examples(examples)

# 📈 Final Summary
avg_score = sum(eval_history) / len(eval_history)
perfect_matches = sum([1 for s in eval_history if s == 1.0])

print("\n📊 Run Summary:")
print(f"Total Samples: {len(dataset)}")
print(f"Average Feedback Score: {round(avg_score, 2)}")
print(f"Perfect Matches: {perfect_matches}/{len(dataset)}")
print(f"📥 Memory Updated: {len(examples)} total few-shot examples saved.")
