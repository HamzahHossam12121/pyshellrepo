import os
import platform
import sys
import getpass
import shutil
from colorama import Fore, Style

def cmd_cd(args, *_):
    try:
        if not args:
            os.chdir(os.path.expanduser("~"))
        else:
            os.chdir(args[0])
    except Exception as e:
        yield f"{Fore.RED}cd: {e}{Style.RESET_ALL}"

def cmd_help(args, input_lines=None, all_commands=None):
    yield f"{Fore.YELLOW}Busybox commands:{Style.RESET_ALL}"
    for c in sorted(COMMANDS.keys()):
        yield f"  {Fore.CYAN}{c}{Style.RESET_ALL}"
    if all_commands:
        others = sorted(set(all_commands.keys()) - set(COMMANDS.keys()))
        if others:
            yield f"\n{Fore.YELLOW}Other extensions:{Style.RESET_ALL}"
            for name in others:
                yield f"  {Fore.GREEN}{name}{Style.RESET_ALL}"

def cmd_cat(args, *_):
    if not args:
        yield f"{Fore.RED}cat: missing file operand{Style.RESET_ALL}"
        return
    for fname in args:
        try:
            with open(fname, encoding='utf-8') as f:
                for line in f:
                    yield line.rstrip()
        except Exception as e:
            yield f"{Fore.RED}cat: {fname}: {e}{Style.RESET_ALL}"

def cmd_ls(args, *_):
    path = args[0] if args else os.getcwd()
    try:
        entries = sorted(os.listdir(path))
        for e in entries:
            full_path = os.path.join(path, e)
            if os.path.isdir(full_path):
                yield f"{Fore.BLUE}{e}{Style.RESET_ALL}"
            else:
                yield f"{Fore.WHITE}{e}{Style.RESET_ALL}"
    except Exception as e:
        yield f"{Fore.RED}ls: {e}{Style.RESET_ALL}"

def cmd_clear(args, *_):
    os.system('cls' if os.name == 'nt' else 'clear')
    return []

def cmd_cp(args, *_):
    if len(args) < 2:
        yield f"{Fore.RED}cp: missing file or destination{Style.RESET_ALL}"
        return
    *srcs, dest = args
    for src in srcs:
        try:
            if os.path.isdir(src):
                shutil.copytree(src, os.path.join(dest, os.path.basename(src)), dirs_exist_ok=True)
            else:
                shutil.copy2(src, dest)
        except Exception as e:
            yield f"{Fore.RED}cp: {e}{Style.RESET_ALL}"

def cmd_mkdir(args, *_):
    if not args:
        yield f"{Fore.RED}mkdir: missing operand{Style.RESET_ALL}"
        return
    for path in args:
        try:
            os.makedirs(path, exist_ok=True)
        except Exception as e:
            yield f"{Fore.RED}mkdir: {e}{Style.RESET_ALL}"

def cmd_rm(args, *_):
    for path in args:
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
        except Exception as e:
            yield f"{Fore.RED}rm: {e}{Style.RESET_ALL}"

def cmd_rmdir(args, *_):
    for path in args:
        try:
            os.rmdir(path)
        except Exception as e:
            yield f"{Fore.RED}rmdir: {e}{Style.RESET_ALL}"

def cmd_mv(args, *_):
    if len(args) < 2:
        yield f"{Fore.RED}mv: missing source or destination{Style.RESET_ALL}"
        return
    src, dest = args
    try:
        shutil.move(src, dest)
    except Exception as e:
        yield f"{Fore.RED}mv: {e}{Style.RESET_ALL}"

def cmd_touch(args, *_):
    if not args:
        yield f"{Fore.RED}touch: missing file operand{Style.RESET_ALL}"
        return
    for fname in args:
        try:
            with open(fname, 'a'):
                os.utime(fname, None)
        except Exception as e:
            yield f"{Fore.RED}touch: {e}{Style.RESET_ALL}"

def cmd_echo(args, *_):
    yield ' '.join(args)

def cmd_pwd(args, *_):
    yield os.getcwd()

def cmd_whoami(args, *_):
    yield getpass.getuser()

def cmd_basename(args, *_):
    if not args:
        yield f"{Fore.RED}basename: missing operand{Style.RESET_ALL}"
    else:
        yield os.path.basename(args[0])

def cmd_dirname(args, *_):
    if not args:
        yield f"{Fore.RED}dirname: missing operand{Style.RESET_ALL}"
    else:
        yield os.path.dirname(args[0])

def cmd_head(args, *_):
    if not args:
        yield f"{Fore.RED}head: missing file operand{Style.RESET_ALL}"
        return
    fname = args[0]
    lines = int(args[1]) if len(args) > 1 else 10
    try:
        with open(fname, encoding='utf-8') as f:
            for i, line in enumerate(f):
                if i >= lines:
                    break
                yield line.rstrip()
    except Exception as e:
        yield f"{Fore.RED}head: {e}{Style.RESET_ALL}"

def cmd_tail(args, *_):
    if not args:
        yield f"{Fore.RED}tail: missing file operand{Style.RESET_ALL}"
        return
    fname = args[0]
    lines = int(args[1]) if len(args) > 1 else 10
    try:
        with open(fname, encoding='utf-8') as f:
            all_lines = f.readlines()
            for line in all_lines[-lines:]:
                yield line.rstrip()
    except Exception as e:
        yield f"{Fore.RED}tail: {e}{Style.RESET_ALL}"

def cmd_busybox(args, *_):
    yield f"{Fore.YELLOW}Pseudo Busybox (Busybox-like){Style.RESET_ALL}"
    yield f"{Fore.CYAN}A lightweight busybox-inspired shell extension for Python Shell.{Style.RESET_ALL}"
    yield ""
    yield f"{Fore.YELLOW}Supported commands:{Style.RESET_ALL}"
    for c in sorted(COMMANDS.keys()):
        yield f"  {Fore.GREEN}{c}{Style.RESET_ALL}"
    yield ""
    yield f"{Fore.YELLOW}Shell info:{Style.RESET_ALL}"
    yield f"  Python version: {platform.python_version()}"
    yield f"  Platform: {platform.system()} {platform.release()}"
    yield f"  Current user: {getpass.getuser()}"
    yield f"  Current directory: {os.getcwd()}"
    yield ""
    yield f"{Fore.MAGENTA}Type 'help' to see all commands.{Style.RESET_ALL}"

# Command map
COMMANDS = {
    "cd": cmd_cd,
    "help": cmd_help,
    "cat": cmd_cat,
    "ls": cmd_ls,
    "clear": cmd_clear,
    "cp": cmd_cp,
    "mkdir": cmd_mkdir,
    "rm": cmd_rm,
    "rmdir": cmd_rmdir,
    "mv": cmd_mv,
    "touch": cmd_touch,
    "echo": cmd_echo,
    "pwd": cmd_pwd,
    "whoami": cmd_whoami,
    "basename": cmd_basename,
    "dirname": cmd_dirname,
    "head": cmd_head,
    "tail": cmd_tail,
    "busybox": cmd_busybox,
}

def register(shell_commands):
    for name, func in COMMANDS.items():
        def make_wrapper(f, cmd_name=name):
            def wrapper(args, print_func):
                try:
                    if cmd_name == "help":
                        result = f(args, all_commands=shell_commands)
                    else:
                        result = f(args)
                    for line in result:
                        print_func(line)
                except Exception as e:
                    print_func(f"{Fore.RED}{cmd_name}: {e}{Style.RESET_ALL}")
            return wrapper
        shell_commands[name] = make_wrapper(func)
