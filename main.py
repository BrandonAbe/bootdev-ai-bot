import sys
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from call_function import available_functions, call_function
from prompts import system_prompt
from config import MAX_ITERATIONS



def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt),
    )

    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
    print("Response:")

    # Add each candidate's content (e.g., function call requests) to the messages for the next iteration
    if response.candidates:
        for candidate in response.candidates:
            function_call_content = candidate.content
            messages.append(function_call_content)
    
    # Handle if there are no function calls by just returning the text response from the model
    if not response.function_calls:
        return response.text
    
    function_responses = []  # Collect valid function call responses to send back to the model
    for function_call_part in response.function_calls:
        # Debug: Print the working directory being used
        # print("Current working directory: ", os.getcwd())
        function_call_result = call_function(function_call_part, verbose)
        # Each function_call_result.parts is a list of Part objects (i.e. should contain function_response)
        for part in function_call_result.parts:
            # Ensure the part has a function_response attribute before accessing it
            if not hasattr(part, "function_response") or part.function_response is None:
                raise Exception("Function call did not return a valid function_response.")
            if verbose:
                # Print the actual function response for debugging/trace
                print(f"-> {part.function_response.response}")
            function_responses.append(part)
    
    # If no valid function responses were collected, raise an error
    if not function_responses:
        raise Exception("No valid function responses were obtained from function calls, exiting...")

    # Add all function responses as a new message with role "function" for the next model iteration
    messages.append(types.Content(role="function", parts=function_responses))

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

    if verbose:
        print(f"User prompt: {user_prompt}\n")

    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)]),]

    # Handle multiple iterations up to MAX_ITERATIONS
    iter_count = 0
    while True:
        iter_count += 1
        if iter_count > MAX_ITERATIONS:
            print(f"Reached maximum allowed iterations ({MAX_ITERATIONS}). Stopping.")
            sys.exit(1)
        
        # Check if response.text is not None before proceeding
        try:
            final_response = generate_content(client, messages, verbose)
            if final_response:
                print(f"Final Response: ", final_response)
                break  # Exit loop if we have a valid final response
        except Exception as e:
            print(f"Error during content generation:", e)
                

if __name__ == "__main__":
    main()