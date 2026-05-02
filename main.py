import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("No API key found!")
client = genai.Client(api_key=api_key)


def main():
    prompt = input("Input prompt: ")
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt)
    
    if not response.usage_metadata:
        raise RuntimeError("API request failed")

    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print(response.text)


if __name__ == "__main__":
    main()
