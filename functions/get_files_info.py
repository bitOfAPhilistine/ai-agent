import os


def get_files_info(working_directory, directory="."):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        # Will be True or False
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        output_text = ["Result for current directory:"]
        for f in os.listdir(target_dir):
            output_text.append(f"- {f}: file_size={os.path.getsize(f"{target_dir}/{f}")}, is_dir={os.path.isdir(f"{target_dir}/{f}")}")
        return "\n".join(output_text)
    except Exception as e:
        return f'Error: {e}'