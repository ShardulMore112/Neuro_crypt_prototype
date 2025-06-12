import requests

class DecoderAgentB:
    def __init__(self, groq_api_key):
        self.api_key = groq_api_key
        self.url = "https://api.groq.com/openai/v1/chat/completions"

    def decode(self, examples, target):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # Construct few-shot prompt
        prompt = (
            "You are a decoding AI that analyzes encrypted patterns and tries to reverse-engineer the encoding rules.\n"
            "You are provided with a few encrypted and original word pairs. From these, deduce the transformation rule.\n"
            "Then decode the given new encrypted word using the same rule.\n"
            "Respond ONLY with the final decoded word (no explanation).\n\n"
        )

        for i, ex in enumerate(examples):
            prompt += f"Example {i+1}:\n  Encoded: {ex['encoded']}\n  Plain:   {ex['plain']}\n\n"

        prompt += f"New Encrypted Word: {target}\nPlain:"

        try:
            response = requests.post(self.url, headers=headers, json={
                "model": "llama3-8b-8192",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an expert at decoding encrypted strings based on given examples. Output only the decoded word."
                    },
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.2,
                "max_tokens": 20
            })

            response.raise_for_status()
            result = response.json()

            if "choices" in result:
                return result["choices"][0]["message"]["content"].strip()
            elif "error" in result:
                print("❌ Groq API Error:", result["error"]["message"])
                return "error"
            else:
                print("⚠️ Unexpected response structure:", result)
                return "error"

        except requests.exceptions.RequestException as e:
            print("🚨 Request failed:", e)
            return "error"
        except Exception as e:
            print("🔴 Unexpected error:", e)
            return "error"


# Optional utility function if you're calling it standalone
def call_groq_llama(prompt, api_key):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "You are a decoding agent, skilled in analyzing encrypted patterns."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.5,
        "max_tokens": 100
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()

        if "choices" in result:
            return result["choices"][0]["message"]["content"].strip()
        elif "error" in result:
            print("❌ Groq API Error:", result["error"]["message"])
            return "error"
        else:
            print("⚠️ Unexpected structure:", result)
            return "error"

    except requests.exceptions.RequestException as e:
        print("🚨 Request failed:", e)
        return "error"
    except Exception as e:
        print("🔴 Unexpected error:", e)
        return "error"
