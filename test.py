import openai
openai.api_key = "your-api-key-here"

try:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello"}],
        max_tokens=5
    )
    print("API key is valid!")
except Exception as e:
    print(f"API key error: {e}")