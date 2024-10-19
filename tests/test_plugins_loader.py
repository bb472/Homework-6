import os
import pytest

from plugins.plugins_loader import load_plugins

def test_load_plugins_success(mocker):
    mocker.patch("os.listdir", return_value=["plugin1.py", "plugin2.py", "__init__.py"])
    mock_import = mocker.patch("importlib.import_module")

    load_plugins()

    mock_import.assert_any_call("plugins.plugin1")
    mock_import.assert_any_call("plugins.plugin2")
    assert mock_import.call_count == 2

def test_load_plugins_directory_not_exist(mocker):
    mocker.patch("os.path.exists", return_value=False)
    mock_print = mocker.patch("builtins.print")

    load_plugins()

    mock_print.assert_called_once_with("Plugins directory 'plugins' does not exist. Skipping plugin loading.")



