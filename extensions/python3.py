import subprocess
import os
import sys

def python3_main(args, print_func):
    if args:
        # Run the specified script with arguments
        script = args[0]
        script_args = args[1:]
        if not os.path.isfile(script):
            print_func(f"python3: file not found: {script}")
            return
        cmd = [sys.executable, script] + script_args
    else:
        # Launch interactive Python shell
        cmd = [sys.executable]

    try:
        subprocess.run(cmd)
    except Exception as e:
        print_func(f"python3: error: {e}")

def register(commands):
    commands["python3"] = lambda args, print_func: python3_main(args, print_func)
