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
    
    function_responses = [] # Initialize function_response list
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)
        try:
            function_response = function_call_result.parts[0].function_response.response
        except AttributeError:
            raise RuntimeError("Runtime Error: Function call did not return a response.")
        # Print with actual newlines if string contains literal \n
        if isinstance(function_response, dict) and "result" in function_response:
            result = function_response["result"]
            if isinstance(result, str):
                print("-> Function response:\n", result.replace("\\n", "\n"))
            else:
                print("-> Function response:", result)
            function_responses.append(function_response)
        else:
            print("-> Function response:", function_response)
            function_responses.append(function_response)
    for function_response in function_responses:
        messages.append(
            types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name="function_response",
                    response=function_response
                )
            ]
        )
    )
    return response.text

def main():
    load_dotenv()
    gemini_key = os.getenv("GEMINI_API_KEY")
    if not gemini_key or gemini_key.strip('"').strip() in {"", "YOUR_KEY_HERE"}:
        raise RuntimeError(
        "GEMINI_API_KEY is not set. Please edit your .env file "
        "and replace YOUR_KEY_HERE with your actual API key."
        )
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

    # Generate updated response to feed LLM again
    final_result = generate_content(client, messages, verbose)
    # Check if response.text is not None before printing
    if final_result:
        print(final_result)

if __name__ == "__main__":
    main()