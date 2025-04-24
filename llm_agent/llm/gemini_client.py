import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from rate_limit.rate_limiter import RateLimiter

load_dotenv()

# Instantiate once (global or per engine)
rate_limiter = RateLimiter()

memory = {}

def call_gemini(prompt):
    """LLM agent with memory, calls Gemini 2.0 Flash via Generative AI SDK."""
    global memory
    if prompt in memory:
        # print("🔁 Retrieved from memory.")
        return memory[prompt]

    rate_limiter.wait_if_needed()

    print("🔮 Calling Gemini API...")
    rate_limiter.record_call()

    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[prompt],
        config=types.GenerateContentConfig(
            max_output_tokens=200,
            temperature=0.3,
            top_k=20
        )
    )

    try:
        result = response.candidates[0].content.parts[0].text
    except Exception as e:
        print("⚠️ Error parsing LLM response:", e)
        result = ""

    memory[prompt] = result
    return result