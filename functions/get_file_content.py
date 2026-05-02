import os
from config import MAX_CHARS


def get_file_content(working_directory, file_path):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        abs_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # Will be True or False
        valid_file_path = os.path.commonpath([working_dir_abs, abs_path]) == working_dir_abs
        if not valid_file_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(abs_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(abs_path) as file:
            return file.read(MAX_CHARS)
    except Exception as e:
        return f'Error: {e}'