import os
from dotenv import load_dotenv
from google import genai
import sys

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    if len(sys.argv) > 1:
        prompt = client.models.generate_content(model="gemini-2.0-flash-001",contents=sys.argv[1])
        print(f"Prompt tokens: {prompt.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {prompt.usage_metadata.candidates_token_count}")
        print("Response:")
        print(prompt.text)
    else:
        print("No arguments provided.")
        sys.exit(1)

if __name__ == "__main__":
    main()