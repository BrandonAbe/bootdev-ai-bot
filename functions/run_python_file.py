import os
import subprocess

def run_python_file(working_directory:str, file_path:str, args=None):
    abs_working_dir = os.path.abspath(working_directory) # Convert to abs path

    '''Construct the full path of file_path relative to working_directory and 
    converts it into an absolute path.'''
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    
    if not file_path.endswith(".py"):
        f'Error: "{file_path}" is not a Python file.'

    try:
        commands = ["python3", abs_file_path]
        if args:
            commands.extend(args) # Add args to end of commands list
        result = subprocess.run(
            commands,
            capture_output=True, #Captures stdout and stderr
            timeout=30,
            text=True, # Allow stdout and stderr to be treated as text string instead of raw bytes
            cwd=abs_working_dir, # Set current working directory
        )
        output = []
        if result.stdout:
            output.append(f"\nSTDOUT: {result.stdout}")
        if result.stderr:
            output.append(f"\nSTDERR: {result.stderr}")
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")
        return "\n".join(output) if output else "No output produced."

    except Exception as e:
        return f"Error: executing Python file: {e}"