# plugins/plugin_loader.py
import importlib
import os

def load_plugins():
    plugins_dir = "plugins"
    if not os.path.exists(plugins_dir):
        print(f"Plugins directory '{plugins_dir}' does not exist. Skipping plugin loading.")
        return

    for file in os.listdir(plugins_dir):
        if file.endswith(".py") and file != "__init__.py":
            plugin_name = file[:-3]  # Remove the .py extension
            try:
                # Import the plugin module dynamically
                importlib.import_module(f"{plugins_dir}.{plugin_name}")
            except ImportError as e:
                print(f"Failed to load plugin {plugin_name}: {e}")
