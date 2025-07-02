import os
import sys
import ctypes
import subprocess

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False

def cmd_su(args, print_func):
    if os.name != 'nt':
        print_func("su extension only supports Windows.")
        return
    
    if is_admin():
        print_func("You are already running as Administrator.")
        return

    print_func("Requesting Administrator privileges...")

    # Relaunch current python script as admin
    script = os.path.abspath(sys.argv[0])
    params = ' '.join(f'"{arg}"' for arg in sys.argv[1:])

    # Use ShellExecute 'runas' to get admin rights
    try:
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, f'"{script}" {params}', None, 1)
    except Exception as e:
        print_func(f"Failed to elevate: {e}")
        return

def register(commands):
    commands["su"] = cmd_su
