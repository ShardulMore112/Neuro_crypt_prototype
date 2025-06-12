
import time
from agentA import EncoderAgentA
from agentB import DecoderAgentB
from feedback import FeedbackEvaluator

# 🧠 Initialize Components
encoder = EncoderAgentA()
decoder = DecoderAgentB(groq_api_key="your_groq_api_key_here")
evaluator = FeedbackEvaluator()

# 🧪 Batch Mode Dataset
dataset = encoder.generate_dataset(samples=20)

# 📊 Tracking Learning History
examples = []  # Few-shot prompt examples for LLM
eval_history = []

print("\n🔁 NeuroCrypt-RL Feedback Loop Running...\n")

def safe_decode_with_retry(decoder, examples, encoded, retries=3, delay=2):
    for attempt in range(retries):
        try:
            prediction = decoder.decode(examples, encoded)
            if prediction != "error":
                return prediction
        except Exception as e:
            print(f"⚠️ Decode attempt {attempt + 1} failed: {e}")
        print(f"⏳ Retry {attempt+1} after {delay} seconds...")
        time.sleep(delay)
    return "error"

for i, sample in enumerate(dataset):
    print(f"[{i+1}] Plain: {sample['plain']} | Encoded: {sample['encoded']} | Rule: {sample['rule_name']}")

    # Decode using Agent B with retry and delay
    prediction = safe_decode_with_retry(decoder, examples, sample['encoded'])

    # Feedback evaluation
    feedback = evaluator.give_feedback(prediction, sample['plain'])
    eval_history.append(feedback['score'])

    print(f"🔍 Predicted: {prediction} | Feedback: {feedback['feedback']}\n")

    # Update few-shot examples if decoding was weak
    if feedback['score'] < 1.0:
        examples.append({"encoded": sample['encoded'], "plain": sample['plain']})

    time.sleep(2.1)  # To respect Groq's 30 RPM limit

# 📈 Summary
avg_score = sum(eval_history) / len(eval_history)
perfect_matches = sum([1 for s in eval_history if s == 1.0])

print("\n📊 Run Summary:")
print(f"Total Samples: {len(dataset)}")
print(f"Average Feedback Score: {round(avg_score, 2)}")
print(f"Perfect Matches: {perfect_matches}/{len(dataset)}")
