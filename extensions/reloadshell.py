import os
import glob
import importlib.util

# This will track commands added by extensions
extension_commands = set()

def register(commands):
    # Hook: extensions must add their commands through this wrapper
    # So we can track which commands come from extensions
    def track_register_command(name, func):
        commands[name] = func
        extension_commands.add(name)

    # Replace the normal register function signature of other extensions with a wrapper
    # So when we reload, we clear extension_commands first, then reload extensions fresh

    def cmd_reloadshell(args, print_func):
        # Remove old extension commands
        for cmd in list(extension_commands):
            if cmd in commands:
                del commands[cmd]
        extension_commands.clear()

        ext_dir = os.path.join(os.path.dirname(__file__), "")
        files = glob.glob(os.path.join(ext_dir, "*.py"))

        for file_path in files:
            name = os.path.splitext(os.path.basename(file_path))[0]
            if name == "reloadshell":
                continue  # skip self

            try:
                spec = importlib.util.spec_from_file_location(name, file_path)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                if hasattr(mod, "register"):
                    # Provide commands dict wrapped with tracking to extension register function
                    mod.register(ExtensionCommandWrapper(commands, extension_commands))
                    print_func(f"[EXTENSION] Reloaded {name}")
            except Exception as e:
                print_func(f"[EXTENSION] Failed to reload {name}: {e}")

        print_func("Reloaded all extensions!")

    commands["reloadshell"] = cmd_reloadshell

# Helper class to wrap the commands dict and track extension commands added
class ExtensionCommandWrapper:
    def __init__(self, commands_dict, ext_cmd_set):
        self.commands = commands_dict
        self.ext_cmd_set = ext_cmd_set
    def __setitem__(self, key, value):
        self.commands[key] = value
        self.ext_cmd_set.add(key)
    def __getitem__(self, key):
        return self.commands[key]
    def __delitem__(self, key):
        del self.commands[key]
        self.ext_cmd_set.discard(key)
    def __contains__(self, key):
        return key in self.commands
    def keys(self):
        return self.commands.keys()
