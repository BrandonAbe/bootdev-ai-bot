import os

def get_files_info(working_directory:str, directory:str=None):
    if directory not in working_directory:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(directory):
        return f'Error: "{directory}" is not a directory'

    contents = []
    
    # Left off on Ch2_L2_step4. To be continued...