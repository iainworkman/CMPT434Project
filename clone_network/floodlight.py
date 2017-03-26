from requests import get

class FloodlightController:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self._switches = None
        self._devices = None
        self._switch_links = None

    @property
    def switches(self):
        """
        switch = {
            "label": None,
            "mac": None
        }
        """
        if not self._switches:
            self._switches = self._request('/wm/core/controller/switches/json')

        switches = []

        for raw in self._switches:
            mac = raw.get('switchDPID').replace(':','')
            switch = {
                'label': 's' + str(int(mac)),
                'mac': mac
            }
            switches.append(switch)

        return switches

    @property
    def devices(self):
        """
        device = {
            "label": None,
            "mac": None,
        }
        """
        if not self._devices:
            self._devices = self._request('/wm/device/').get('devices')

        devices = []
        # TODO: find a way to figure out host id from MAC
        label_id = 1
        for raw in self._devices:
            mac = raw.get('mac')[0].replace(':','')
            device = {
                'label': 'h' + str(label_id),
                'mac': mac
            }
            devices.append(device)
            label_id += 1

        return devices

    def _get_label_from_mac(self, mac):
        nodes = self.devices + self.switches
        return [ n["label"] for n in nodes if n["mac"] == mac ][0]

    @property
    def links(self):
        """
        link = {
            "src_label": None,
            "src_port": None,
            "dst_label": None,
            "dst_port": None
        }
        """
        if not self._switch_links:
            self._switch_links = self._request('/wm/topology/links/json')
        if not self._devices:
            self._devices = self._request('/wm/device/').get('devices')

        links = []
        for raw in self._switch_links:
            src_mac = raw.get('src-switch').replace(':','')
            dst_mac = raw.get('dst-switch').replace(':','')
            link = {
                'src_label': self._get_label_from_mac(src_mac),
                'src_port': int(raw.get('src-port')),
                'dst_label': self._get_label_from_mac(dst_mac),
                'dst_port': int(raw.get('dst-port'))
            }
            links.append(link)

        for raw_d in self._devices:
            for raw in raw_d.get('attachmentPoint'):
                src_mac = raw_d.get('mac')[0].replace(':','')
                dst_mac = raw.get('switch').replace(':','')
                link = {
                    'src_label': self._get_label_from_mac(src_mac),
                    'src_port': None,
                    'dst_label': self._get_label_from_mac(dst_mac),
                    'dst_port': int(raw.get('port'))
                }
                links.append(link)

        return links

    def _request(self, endpoint):

        full_url = 'http://{controller_ip}:{controller_port}{endpoint}'.format(
            controller_ip=self.ip,
            controller_port=self.port,
            endpoint=endpoint
        )

        response = get(full_url)

        response.raise_for_status()

        return response.json()

if __name__ == "__main__":
    f = FloodlightController("localhost", "8100")
    print(f.switches)
    print(f.devices)
    print(f.links)

