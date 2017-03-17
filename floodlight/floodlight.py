from requests import get


class FloodlightSwitch:

    def __init__(self, dpid):
        self.dpid = dpid


class FloodlightHost:

    def __init__(self):
        self.switch_link = None

    def link_to_switch(self, switch):
        self.switch_link = FloodlightLink(self, switch)


class FloodlightLink:

    def __init__(self, device1, device2):
        self.device1 = device1
        self.device2 = device2


class FloodlightController:

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def get_switches(self):
        raw_switches = self._floodlight_request('/wm/core/controller/switches/json').json()
        parsed_switches = []

        for raw_switch in raw_switches:
            parsed_switch = FloodlightSwitch(raw_switch.get('switchDPID'))
            parsed_switches.append(parsed_switch)

        return parsed_switches

    def get_hosts(self):
        switches = self.get_switches()
        raw_hosts = self._floodlight_request('/wm/device/').json()
        parsed_hosts = []

        for raw_host in raw_hosts:
            if raw_host.get('attachment_point'):
                parsed_host = FloodlightHost()

                # Find linked switch:
                for switch in switches:
                    if switch.dpid == raw_host.get('attachment_point').get('switch'):
                        parsed_host.link_to_switch(switch)
                        break

                parsed_hosts.append(parsed_host)

        return parsed_hosts

    def get_switch_links(self):
        raw_switch_links = self._floodlight_request('/wm/topology/links/json').json()
        parsed_switch_links = []
        switches = self.get_switches()

        for raw_switch_link in raw_switch_links:
            device1 = None
            device2 = None

            for switch in switches:
                if raw_switch_link.get('dst-switch') == switch.dpid:
                    device1 = switch

                if raw_switch_link.get('src-switch') == switch.dpid:
                    device2 = switch

            if device1 and device2:
                parsed_switch_link = FloodlightLink(device1, device2)

                parsed_switch_links.append(parsed_switch_links)

        return parsed_switch_links

    def _floodlight_request(self, endpoint):

        full_url = 'http://{controller_ip}:{controller_port}{endpoint}'.format(
            controller_ip=self.ip,
            controller_port=self.port,
            endpoint=endpoint
        )

        response = get(full_url)

        response.raise_for_status()

        return response
