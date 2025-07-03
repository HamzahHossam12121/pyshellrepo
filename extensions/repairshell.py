import os
import glob
import importlib.util
from time import sleep
from colorama import Fore, Style

# We'll import requests with a fallback in case it's missing
try:
    import requests
except ImportError:
    requests = None

REPO_BASE = "https://raw.githubusercontent.com/HamzahHossam12121/pyshellrepo/main/extensions/"
CORE_FILES = [
    "su.py",
    "busybox.py",
    "pkg.py",
    "python3.py",
    "reloadshell.py",
    "sh.py",
    "__init__.py"
]

def download_file(url, dest, print_func, retries=3, delay=2):
    if requests is None:
        print_func(f"{Fore.RED}Error: 'requests' module not installed. Please install it with 'pip install requests'.{Style.RESET_ALL}")
        return False
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
            response.raise_for_status()
            with open(dest, 'wb') as f:
                f.write(response.content)
            print_func(f"{Fore.GREEN}Downloaded: {os.path.basename(dest)}{Style.RESET_ALL}")
            return True
        except Exception as e:
            print_func(f"{Fore.YELLOW}Attempt {attempt} failed to download {os.path.basename(dest)}: {e}{Style.RESET_ALL}")
            if attempt < retries:
                sleep(delay)
    print_func(f"{Fore.RED}Failed to download {os.path.basename(dest)} after {retries} attempts.{Style.RESET_ALL}")
    return False

def repairshell_command(args, print_func):
    print_func(f"{Fore.YELLOW}Repairing core shell files...{Style.RESET_ALL}")

    ext_dir = os.path.dirname(__file__)
    commands = globals().get("COMMANDS", None)
    if commands is None:
        print_func(f"{Fore.RED}Internal error: COMMANDS not found.{Style.RESET_ALL}")
        return

    success, fail = 0, 0
    for fname in CORE_FILES:
        url = REPO_BASE + fname
        dest = os.path.join(ext_dir, fname)
        if download_file(url, dest, print_func):
            success += 1
        else:
            fail += 1

    print_func(f"\n{Fore.YELLOW}Reloading extensions...{Style.RESET_ALL}")

    for cmd in list(commands.keys()):
        if cmd != "repairshell":
            del commands[cmd]

    for file_path in glob.glob(os.path.join(ext_dir, "*.py")):
        name = os.path.splitext(os.path.basename(file_path))[0]
        if name == "repairshell":
            continue
        try:
            spec = importlib.util.spec_from_file_location(name, file_path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            if hasattr(mod, "register"):
                mod.register(commands)
                print_func(f"{Fore.MAGENTA}[EXTENSION] Reloaded {name}{Style.RESET_ALL}")
        except Exception as e:
            print_func(f"{Fore.RED}[EXTENSION] Failed to reload {name}: {e}{Style.RESET_ALL}")

    print_func(f"\n{Fore.CYAN}Repair complete: {success} files downloaded, {fail} failed.{Style.RESET_ALL}")

def register(commands):
    commands["repairshell"] = lambda args, print_func: repairshell_command(args, print_func)
    globals()["COMMANDS"] = commands
