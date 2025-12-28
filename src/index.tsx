import {
  definePlugin,
  PanelSection,
  PanelSectionRow,
  ServerAPI,
  staticClasses,
  ButtonItem,
} from "decky-frontend-lib";

import {
  VFC,
  useEffect,
  useState
} from "react";

import { FaShieldAlt } from "react-icons/fa";

type Device = {
  id: string,
  name: string,
}

const Content: VFC<{ serverAPI: ServerAPI }> = ({ serverAPI }) => {

  const [ loaded, setLoaded ] = useState(false);
  const [ devices, setDevices ] = useState<Device[]>([]);

  const loadDevices = async () => {
    try {
      const response = await serverAPI.callPluginMethod<{}, Device[]>('show', {});
      const devices = response.result as Device[];

      setDevices(devices);
    } catch (error) {
      console.error(error);
    }

    setLoaded(true);
  }

  const toggleBind = async (device: Device, switchValue: boolean) => {
    await serverAPI.callPluginMethod((switchValue) ? 'up' : 'down', { id: device.id });
  }

  useEffect(() => {
    loadDevices();
  }, []);

  return (
    <>
      <PanelSection title="Devices">

        {loaded && devices.length == 0 && <PanelSectionRow>
          No Devices Found
        </PanelSectionRow>}

        {devices.length > 0 && devices.map((device) => (
          <PanelSectionRow>
            {device.name}
            <ButtonItem onClick={() => {
              toggleBind(device, true)
            }}>
            Bind {device.id}
            </ButtonItem>
            <ButtonItem onClick={() => {
              toggleBind(device, false)
            }}>
            Unbind {device.id}
            </ButtonItem>
          </PanelSectionRow>
        ))}

      </PanelSection>
      <PanelSection title="Settings">
        <PanelSectionRow>
          <ButtonItem onClick={() => {
            loadDevices()
          }}>
          Reload USB devices
          </ButtonItem>
        </PanelSectionRow>

      </PanelSection>
    </>
  );
};

export default definePlugin((serverApi: ServerAPI) => {
  return {
    title: <div className={staticClasses.Title}>DeckyUSBIP</div>,
    content: <Content serverAPI={serverApi} />,
    icon: <FaShieldAlt />,
  };
});
