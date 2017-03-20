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
        if not self._switches:
            self._switches = self._floodlight_request('/wm/core/controller/switches/json').json()

        return self._switches

    @property
    def devices(self):
        if not self._devices:

            self._devices = self._floodlight_request('/wm/device/').json()

        return self._devices

    @property
    def switch_links(self):

        if not self._switch_links:
            self._switch_links = self._floodlight_request('/wm/topology/links/json').json()

        return self._switch_links

    def _floodlight_request(self, endpoint):

        full_url = 'http://{controller_ip}:{controller_port}{endpoint}'.format(
            controller_ip=self.ip,
            controller_port=self.port,
            endpoint=endpoint
        )

        response = get(full_url)

        response.raise_for_status()

        return response
