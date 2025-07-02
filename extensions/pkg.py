# extensions/pkg.py
import requests
import os
from colorama import Fore, Style

# The base raw GitHub folder URL
REPO_RAW_URL = "https://raw.githubusercontent.com/HamzahHossam12121/pyshellrepo/main/extensions"

def pkg_search(args, input_lines=None):
    if not args:
        yield f"{Fore.YELLOW}Usage: pkg search <extension-name>{Style.RESET_ALL}"
        return
    query = args[0].lower()
    try:
        response = requests.get("https://api.github.com/repos/HamzahHossam12121/pyshellrepo/contents/extensions")
        response.raise_for_status()
        data = response.json()
        found = False
        for file in data:
            if query in file['name'].lower():
                yield f"{Fore.CYAN}Found: {file['name']}{Style.RESET_ALL}"
                found = True
        if not found:
            yield f"{Fore.RED}No matches found for '{query}'{Style.RESET_ALL}"
    except Exception as e:
        yield f"{Fore.RED}Search failed: {e}{Style.RESET_ALL}"

def pkg_install(args, input_lines=None):
    if not args:
        yield f"{Fore.YELLOW}Usage: pkg install <extension-name>{Style.RESET_ALL}"
        return
    name = args[0]
    url = f"{REPO_RAW_URL}/{name}.py"
    dest_path = os.path.join("extensions", f"{name}.py")
    try:
        r = requests.get(url)
        if r.status_code == 404:
            yield f"{Fore.RED}Extension '{name}' not found in repo.{Style.RESET_ALL}"
            return
        with open(dest_path, "w", encoding="utf-8") as f:
            f.write(r.text)
        yield f"{Fore.GREEN}Installed extension '{name}' successfully!{Style.RESET_ALL}"
    except Exception as e:
        yield f"{Fore.RED}Install failed: {e}{Style.RESET_ALL}"

COMMANDS = {
    "pkg": lambda args, input_lines=None: (
        pkg_search(args[1:], input_lines) if args and args[0] == "search"
        else pkg_install(args[1:], input_lines) if args and args[0] == "install"
        else iter([f"{Fore.YELLOW}Usage: pkg <search|install> <name>{Style.RESET_ALL}"])
    )
}

def register(commands):
    for name, func in COMMANDS.items():
        def wrapper(args, print_func, func=func):
            for line in func(args):
                print_func(line)
        commands[name] = wrapper
