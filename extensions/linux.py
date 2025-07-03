# extensions/linux.py

import os
import subprocess
import urllib.request
from colorama import Fore, Style

qemu_proc = None  # Global reference to QEMU process

def download_disk_image(dest_path):
    url = "https://altushost-bul.dl.sourceforge.net/project/gns-3/Qemu%20Appliances/linux-tinycore-11.1.qcow2?viasf=1"
    try:
        yield f"{Fore.YELLOW}Downloading TinyCore Linux image...{Style.RESET_ALL}"
        urllib.request.urlretrieve(url, dest_path)
        yield f"{Fore.GREEN}Download complete! Saved as {dest_path}{Style.RESET_ALL}"
    except Exception as e:
        yield f"{Fore.RED}Failed to download disk image: {e}{Style.RESET_ALL}"

def ensure_disk():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(base_dir, "..", "linuxassets")
    disk_img = os.path.join(assets_dir, "linux.qcow2")

    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)
        yield f"{Fore.GREEN}Created linuxassets directory.{Style.RESET_ALL}"

    if not os.path.isfile(disk_img):
        for line in download_disk_image(disk_img):
            yield line

    yield disk_img  # Return path last

def linux_main(args, input_lines=None):
    global qemu_proc

    disk_path = None
    for step in ensure_disk():
        if step.endswith(".qcow2"):
            disk_path = step
        else:
            yield step  # show log messages

    if not disk_path or not os.path.isfile(disk_path):
        yield f"{Fore.RED}Could not continue without valid disk image.{Style.RESET_ALL}"
        return

    if qemu_proc and qemu_proc.poll() is None:
        yield f"{Fore.YELLOW}QEMU is already running!{Style.RESET_ALL}"
        return

    qemu_cmd = [
        "qemu-system-x86_64",
        "-display", "sdl",  # GUI mode
        "-m", "256M",
        "-drive", f"file={disk_path},format=qcow2"
    ]

    try:
        qemu_proc = subprocess.Popen(
            qemu_cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.DETACHED_PROCESS if os.name == 'nt' else 0
        )
        yield f"{Fore.GREEN}QEMU started in background (PID: {qemu_proc.pid}){Style.RESET_ALL}"
    except Exception as e:
        yield f"{Fore.RED}Failed to start QEMU: {e}{Style.RESET_ALL}"

def register(commands):
    def wrapper(args, print_func):
        for line in linux_main(args):
            print_func(line)
    commands["linux"] = wrapper
