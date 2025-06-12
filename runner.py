from agentB import DecoderAgentB
from feedback import FeedbackEvaluator

# Step 1: Few-shot examples and new target
examples = [
    {"encoded": "h2ll4", "plain": "hello"},
    {"encoded": "w3r7d", "plain": "world"}
]
target = "n2#r1#"
ground_truth = "nerd"  # this is the correct decoded version (from Agent A)

# Step 2: Initialize decoder and run
decoder = DecoderAgentB(groq_api_key="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")
predicted = decoder.decode(examples, target)

print("🧠 Decoded Result:", predicted)

# Step 3: Feedback Evaluation
evaluator = FeedbackEvaluator()
feedback = evaluator.give_feedback(predicted, ground_truth)

# Step 4: Print Feedback
print("\n🔁 Feedback Loop")
print("Match:", feedback["match"])
print("Score:", feedback["score"])
print("Feedback:", feedback["feedback"])
