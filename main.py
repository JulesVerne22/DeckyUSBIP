import subprocess
import logging
from os import path
from settings import SettingsManager
from helpers import get_user

USER = get_user()
HOME_PATH = "/home/" + USER
HOMEBREW_PATH = HOME_PATH + "/homebrew"

logging.basicConfig(filename="/tmp/deckyusbip.log",
                    format='[DeckyUSBIP] %(asctime)s %(levelname)s %(message)s',
                    filemode='w+',
                    force=True)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


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
    logger.info("Running Install Script")
    subprocess.run(["bash", path.dirname(__file__) + "/extensions/install"], cwd=path.dirname(__file__) + "/extensions")


def run_uninstall_script():
    logger.info("Running Uninstall Script")
    subprocess.run(["bash", path.dirname(__file__) + "/extensions/uninstall"], cwd=path.dirname(__file__) + "/extensions")


class Plugin:

    settings: SettingsManager = SettingsManager("deckyusbip", path.join(HOMEBREW_PATH, "settings"))

    async def _main(self):
        logger.info("Running install script if not installed")
        installed = self.settings.getSetting("installed", False)
        if not installed:
            logger.info("Not installed, running install script")
            run_install_script()

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
        result = subprocess.run(["usbip", "bind", "-b", id], text=True, capture_output=True).stdout
        return result

    # Unbinds usb device
    async def down(self, id):
        logger.info("Unbinding device: " + id)
        result = subprocess.run(["usbip", "unbind", "-b", id], text=True, capture_output=True).stdout
        return result

    # Checks if usbip is installed
    async def is_usbip_installed(self):
        try:
            subprocess.run(["usbip", "list", "-l"], check=True)
            return True
        except subprocess.CalledProcessError:
            return False

    # The installed setting
    async def is_plugin_installed(self):
        return self.settings.getSetting("installed", False)

    # Install plugin
    async def install_plugin(self):
        logger.info("Running install script...")
        self.settings.setSetting("installed", True)
        run_install_script()
        return True

    # Uninstall plugin
    async def uninstall_plugin(self):
        logger.info("Running uninstall script...")
        self.settings.setSetting("installed", False)
        run_uninstall_script()
        return True

    # Clean-up on aisle 5
    async def _unload(self):
        subprocess.run(["bash", path.dirname(__file__) + "/extensions/uninstall"], cwd=path.dirname(__file__) + "/extensions")
        pass
