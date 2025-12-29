import {
  ButtonItem,
  PanelSection,
  PanelSectionRow,
  staticClasses
} from "@decky/ui";
import {
  callable,
  definePlugin,
  // routerHook
  toaster,
} from "@decky/api"
import { useState, useEffect } from "react";
import { FaShip } from "react-icons/fa";

// import logo from "../assets/logo.png";

type Device = {
  id: string,
  name: string,
}

const listDevices = callable<[], Device[]>("show");
const bindDevice = callable<[deviceId: string], string>("up");
const unbindDevice = callable<[deviceId: string], string>("down");

function Content() {
  const [loaded, setLoaded] = useState<boolean>(false);
  const [devices, setDevices] = useState<Device[]>([]);

  const loadDevices = async () => {
    try {
      const response = await listDevices();
      setDevices(response);
    } catch (error) {
      console.error(error);
    }

    setLoaded(true);
  }

  useEffect(() => {
    loadDevices();
  }, []);

  return (
    <>
      <PanelSection title="Devices">
        {loaded && devices.length === 0 && <PanelSectionRow>
          No Devices Found
        </PanelSectionRow>}

        {devices.length > 0 && devices.map((device) => (
          <PanelSectionRow>
            {device.name}
            <ButtonItem
              layout="below"
              onClick={() => {
                bindDevice(device.id).then(status => {
                  toaster.toast({
                    title: "Device Bind Status",
                    body: `${status}`
                  });
                }).catch(error => {
                  console.error(error);
                  toaster.toast({
                    title: "Device Bind Error",
                    body: `Error: ${error}`
                  })
                })
              }}>
              Bind {device.id}
            </ButtonItem>
            <ButtonItem
              layout="below"
              onClick={() => {
                unbindDevice(device.id).then(status => {
                  toaster.toast({
                    title: "Device Unbind Status",
                    body: `${status}`
                  });
                }).catch(error => {
                  console.error(error);
                  toaster.toast({
                    title: "Device Unbind Error",
                    body: `Error: ${error}`
                  })
                })
              }}>
              Unbind {device.id}
            </ButtonItem>
          </PanelSectionRow>
        ))}
      </PanelSection>
      <PanelSection title="Settings">
        <PanelSectionRow>
          <ButtonItem
            layout="below"
            onClick={() => {
              loadDevices();
            }}>
            Reload USB devices
          </ButtonItem>
        </PanelSectionRow>
      </PanelSection>
    </>
  );
};

export default definePlugin(() => {
  console.log("DeckyUSBIP plugin initializing")

  return {
    // The name shown in various decky menus
    name: "DeckyUSBIP",
    // The element displayed at the top of your plugin's menu
    titleView: <div className={staticClasses.Title}>DeckyUSBIP</div>,
    // The content of your plugin's menu
    content: <Content />,
    // The icon displayed in the plugin list
    icon: <FaShip />,
    // The function triggered when your plugin unloads
    onDismount() {
      console.log("Unloading")
    },
  };
});
