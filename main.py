import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from get_file_content import schema_get_file_content, get_file_content
from get_files_info import schema_get_files_info, get_files_info
from write_file import schema_write_file, write_file
from run_python_file import schema_run_python_file, run_python_file
from config import SYSTEM_PROMPT


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("No API key found!")
client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()
messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

available_functions = types.Tool(
    function_declarations=[schema_get_files_info],
)

def main():
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            tools=available_functions))
    
    if not response.usage_metadata:
        raise RuntimeError("API request failed")

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print(response.text)

    for function_call in response.function_calls:
        print(f"Calling function: {function_call.name}({function_call.args})")


if __name__ == "__main__":
    main()
