import os
import glob
import importlib.util
import urllib.request
from colorama import Fore, Style

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

def repairshell_command(args, print_func):
    print_func(f"{Fore.YELLOW}Repairing core shell files...{Style.RESET_ALL}")

    ext_dir = os.path.dirname(__file__)
    commands = globals().get("COMMANDS", None)
    if commands is None:
        print_func(f"{Fore.RED}Internal error: COMMANDS not found.{Style.RESET_ALL}")
        return

    # 1. Download files with proper User-Agent header
    success, fail = 0, 0
    for fname in CORE_FILES:
        url = REPO_BASE + fname
        dest = os.path.join(ext_dir, fname)
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response, open(dest, 'wb') as out_file:
                out_file.write(response.read())
            print_func(f"{Fore.GREEN}Downloaded: {fname}{Style.RESET_ALL}")
            success += 1
        except Exception as e:
            print_func(f"{Fore.RED}Failed to download {fname}: {e}{Style.RESET_ALL}")
            fail += 1

    # 2. Reload extensions (manual)
    print_func(f"\n{Fore.YELLOW}Reloading extensions...{Style.RESET_ALL}")

    for cmd in list(commands.keys()):
        if cmd != "repairshell":
            del commands[cmd]

    for file_path in glob.glob(os.path.join(ext_dir, "*.py")):
        name = os.path.splitext(os.path.basename(file_path))[0]
        if name == "repairshell":
            continue  # don't reload itself
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
    globals()["COMMANDS"] = commands  # so repairshell_command can access it
