import os

# The decky plugin module is located at decky-loader/plugin
# For easy intellisense checkout the decky-loader code repo
# and add the `decky-loader/plugin/imports` path to `python.analysis.extraPaths` in `.vscode/settings.json`
import decky
import asyncio
import subprocess
import logging
from os import path
from settings import SettingsManager

settingsDir = decky.DECKY_PLUGIN_SETTINGS_DIR
loggingDir = decky.DECKY_PLUGIN_LOG_DIR
logger = decky.logger

logger.setLevel(logging.DEBUG)
logger.info('[backend] Settings path: {}'.format(settingsDir))
settings = SettingsManager(name="settings", settings_directory=settingsDir)
settings.read()

def device_mapper(xn):
    components = xn.split("\n")
    return {
        "id": components[0].split(' ')[3],
        "name": components[1].lstrip(),
    }

def get_available_devices():
    result = subprocess.run(["usbip", "list", "-l"], text=True, capture_output=True).stdout
    devices = result.split("\n\n")
    devices.pop(-1)
    mapped = map(device_mapper, devices)
    return next(mapped, None)

def run_install_script():
    logger.info("Running install script")
    subprocess.run(["bash", path.dirname(__file__) + "/extensions/install"], cwd=path.dirname(__file__) + "/extensions")

def run_uninstall_script():
    logger.info("Running uninstall script")
    subprocess.run(["bash", path.dirname(__file__) + "/extensions/uninstall"], cwd=path.dirname(__file__) + "/extensions")

class Plugin:
    # Asyncio-compatible long-running code, executed in a task when the plugin is loaded
    async def _main(self):
        logger.info("Running install script if not installed")
        installed = settings.getSetting("installed", False)
        # self.loop = asyncio.get_event_loop()
        if not installed:
            logger.info("Not installed, running install script")
            run_install_script()
            settings.setSetting("installed", True)

    # Function called first during the unload process, utilize this to handle your plugin being stopped, but not
    # completely removed
    async def _unload(self):
        pass

    # Function called after `_unload` during uninstall, utilize this to clean up processes and other remnants of your
    # plugin that may remain on the system
    async def _uninstall(self):
        subprocess.run(["bash", path.dirname(__file__) + "/extensions/uninstall"], cwd=path.dirname(__file__) + "/extensions")
        pass

    # Lists the usb devices from usbip.
    async def show(self):
        result = subprocess.run(["usbip", "list", "-l"], text=True, capture_output=True).stdout
        devices = result.split("\n\n")
        devices.pop(-1)
        mapped = map(device_mapper, devices)
        return list(mapped)
    
    # Binds usb device
    async def up(self, id):
        logger.info("Binding device: " + id)
        result = subprocess.run(["usbip", "bind", "-b", id], text=True, capture_output=True)
        return result.stdout + result.stderr

    # Unbinds usb device
    async def down(self, id):
        logger.info("Unbinding device: " + id)
        result = subprocess.run(["usbip", "unbind", "-b", id], text=True, capture_output=True)
        return result.stdout + result.stderr

    # Checks if usbip is installed
    async def is_usbip_installed(self):
        try:
            subprocess.run(["usbip", "list", "-l"], check=True)
            return True
        except subprocess.CalledProcessError:
            return False

    # The installed setting
    async def is_plugin_installed(self):
        return settings.getSetting("installed", False)

    # Install plugin
    async def install_plugin(self):
        logger.info("Running install script...")
        settings.setSetting("installed", True)
        run_install_script()
        return True
