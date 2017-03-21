# Mininet Docker Image
FROM ubuntu:trusty

MAINTAINER Iain Workman <iain.workman@googlemail.com>

RUN apt-get --assume-yes update
RUN apt-get --assume-yes install mininet net-tools git
RUN git clone git://github.com/mininet/mininet /root/mininet
WORKDIR /root/mininet
RUN git checkout -b 2.2.1 2.2.1
RUN /root/mininet/util/install.sh -nfv
#RUN echo "service openvswitch-switch start" >> /init.sh
#RUN echo "python -E mininet_script.py" >> /init.sh
#RUN chmod +x /init.sh


ENTRYPOINT /init.sh

#RUN echo "/usr/share/openvswitch/scripts/ovs-ctl start --system-id=random" > /init.sh
#RUN chmod +x init.sh


