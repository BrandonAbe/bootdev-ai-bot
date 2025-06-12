import os

def write_file(working_directory:str, file_path:str, content:str):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    try:
        if not os.path.exists(file_path):
            # Create it...
            os.makedirs(file_path)
    except Exception as e:
        return f'Error: {str(e)}'
