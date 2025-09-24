import sys
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from call_function import available_functions, call_function
from prompts import system_prompt


def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt)
    )

    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
    print("Response:")
    
    if not response.function_calls: # check if any available function was used
        return response.text
    
    function_response = [] # Initialize function_response list
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)
        try:
            function_reponse = function_call_result.parts[0].function_response.response
        except AttributeError:
            raise RuntimeError("Runtime Error: Function call did not return a response.")
        # Check if response is a dictionary AND verbose was set...
        if isinstance(function_response, dict) and verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")


def main():
    load_dotenv()
    verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")] # List Comprehension
    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)
    user_prompt = " ".join(args)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {user_prompt}\n")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    generate_content(client, messages, verbose)

if __name__ == "__main__":
    main()