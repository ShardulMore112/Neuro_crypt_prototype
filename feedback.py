# feedback.py

class FeedbackEvaluator:
    def __init__(self):
        pass

    def clean_text(self, text):
        """Utility to clean and normalize decoded outputs."""
        return text.strip().lower()

    def exact_match(self, predicted, actual):
        """Checks if the decoded prediction exactly matches the original plaintext."""
        return self.clean_text(predicted) == self.clean_text(actual)

    def score(self, predicted, actual):
        """
        Returns a feedback score:
        - 1.0: perfect match
        - <1.0: partial match (character-level similarity)
        - 0.0: completely wrong
        """
        predicted = self.clean_text(predicted)
        actual = self.clean_text(actual)

        if not predicted or not actual:
            return 0.0

        if predicted == actual:
            return 1.0

        # Partial match: character-level Jaccard similarity
        pred_chars = set(predicted)
        actual_chars = set(actual)

        intersection = len(pred_chars & actual_chars)
        union = len(pred_chars | actual_chars)

        return round(intersection / union, 2)

    def give_feedback(self, predicted, actual):
        match = self.exact_match(predicted, actual)
        score = self.score(predicted, actual)
        return {
            "match": match,
            "score": score,
            "feedback": "Perfect match!" if match else f"Similarity score: {score}"
        }


# 🧪 Example usage
if __name__ == "__main__":
    fb = FeedbackEvaluator()
    pred = "Neural"
    actual = "neural"
    result = fb.give_feedback(pred, actual)
    print(result)
