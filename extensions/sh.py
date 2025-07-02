# sh.py
import ctypes
from colorama import Fore, Style

def parse_pipeline(command_line):
    parts = [part.strip() for part in command_line.split('|')]
    pipeline = [part.split() for part in parts]
    return pipeline

def run_pipeline(pipeline, command_dict):
    input_lines = None
    for cmd_parts in pipeline:
        if not cmd_parts:
            continue
        cmd_name = cmd_parts[0].lower()
        args = cmd_parts[1:]
        if cmd_name not in command_dict:
            return [f"{Fore.RED}Unknown command: {cmd_name}{Style.RESET_ALL}"]
        try:
            output_lines = command_dict[cmd_name](args, input_lines)
            if not hasattr(output_lines, '__iter__') or isinstance(output_lines, str):
                output_lines = [str(output_lines)]
            input_lines = output_lines
        except Exception as e:
            return [f"{Fore.RED}Error running {cmd_name}: {e}{Style.RESET_ALL}"]
    return list(input_lines)

def run_command(command_line, command_dict):
    pipeline = parse_pipeline(command_line)
    return run_pipeline(pipeline, command_dict)

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False

def get_prompt_symbol():
    return "#" if is_admin() else "$"
