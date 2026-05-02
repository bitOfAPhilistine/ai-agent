import os


def write_file(working_directory, file_path, content):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        abs_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # Will be True or False
        valid_file_path = os.path.commonpath([working_dir_abs, abs_path]) == working_dir_abs
        if not valid_file_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        if os.path.isdir(abs_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        os.makedirs(file_path, exist_ok=True)

        with open(file_path, mode='w') as file:
            file.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {e}'