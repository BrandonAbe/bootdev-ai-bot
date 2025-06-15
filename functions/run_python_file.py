import os

def run_python_file(working_directory:str, file_path:str):
    abs_working_dir = os.path.abspath(working_directory) # Convert to abs path

    '''Construct the full path of file_path relative to working_directory and 
    converts it into an absolute path.'''
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    
    if not file_path.endswith(".py"):
        f'Error: "{file_path}" is not a Python file.'