# DeckyUSBIP

DeckyUSBIP allows you to share USB connections from the USBIP service to your network. It
does require downloading+installing USBIP, and enabling+starting the correlating host service.
From there, the plugin can list the avialable devices and the user can choose which to bind
and unbind.

## Settings

- **List Devices:** Lists the available USB devices and their IDs to share.
- **Bind Device:** Binds the specified USB device by its ID.
- **Unbind Device:** Unbinds the specified USB device by its ID.

## Usage

Follow the USBIP instructions to install USBIP in desktop mode. This should include an
rpmostree install command, a couple modprobe enable commands, and service start and
enable commands.

### Listing, Binding, Unbinding

Once the above is completed, the plugin should be able to list the available devices by
clicking the list devices button. Then you can bind and unbind those devices using their
IDs (ex. 1-1), with the bind and unbind textbox and button.

## Credits

- [Julian Smith] - Developer

## Building the Plugin Manually

```bash
pnpm i
pnpm run build
```
