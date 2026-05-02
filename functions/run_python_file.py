import os
from google import genai
from google.genai import types
import subprocess


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the selected python file, with given args if args are given",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Directory path to the file, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Any additional arguments to run the file with"
            )
        },
    ),
)

def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        abs_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # Will be True or False
        valid_file_path = os.path.commonpath([working_dir_abs, abs_path]) == working_dir_abs
        if not valid_file_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(abs_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if ".py" not in file_path:
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", abs_path]
        if args:
            command = command.extend(args)
        process = subprocess.run(command, capture_output=True, text=True, timeout=30)
        if process.returncode != 0:
            return f"Process exited with code {process.returncode}"
        elif process.stdout == None and process.stderr == None:
            return "No output produced"
        else:
            return f"STDOUT: {process.stdout}\nSTDERR: {process.stderr}"
    except Exception as e:
        return f'Error: {e}'