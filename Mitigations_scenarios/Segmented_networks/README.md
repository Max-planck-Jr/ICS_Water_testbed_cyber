# ICS Testbed Network Segmentation & Customization

This ICS testbed emulates a realistic industrial network for cybersecurity research and training. It consists of multiple containers representing PLCs, SCADA/HMI, physical simulators, and attacker nodes all orchestrated via Docker. The environment supports: 

- Flat network mode (via the default `swat` network)
- Segmented mode using router containers with `iptables` to enforce isolation and security across **Purdue Model-aligned subnets**.

##  Network Topology Overview

In the segmented architecture, each logical ICS zone is assigned a dedicated subnet. Communication between subnets is controlled by router containers, which also function as firewalls using **iptables**

| Zone             | Subnet             | Purpose                              | Routed by     |
|------------------|--------------------|---------------------------------------|---------------|
| Main/Transit     | 172.18.0.0/24      | Backbone network between routers      | —             |
| Device Field     | 172.18.1.0/24      | PLCs and Physical Simulator (Level 0/1) | router_1      |
| Supervisory      | 172.18.2.0/24      | SCADA and HMI systems (Level 2)      | router_1      |
| DMZ              | 172.18.3.0/24      | Gateway or proxy zone                | router_2      |
| IT Department    | 172.18.4.0/24      | Remote admin, monitoring (Level 3/4) | router_3      |


**NB:**  All communication between zones passes through a router/firewall container with fine-grained `iptables` policies. 

## Default Flat Network (swat)

The `create_docker_network.sh` found in the testbed realized by Yi, script sets up a flat swat Docker network (172.18.0.0/24) and launches all services on it.

To deploy
```bash
chmod +x create_docker_network.sh
sudo ./create_docker_network.sh
```

### Custom Segmented Setup (Recommended)

For a segmented deployment, use the additional script:

`create_segmented_networks.sh`
```bash
#!/bin/bash

echo "Creating segmented Docker networks..."

# Main Transit Network
docker network create --subnet=172.18.0.0/24 --gateway=172.18.0.1 scada_network

# Device Field Network (PLCs, MTU)
docker network create --subnet=172.18.1.0/24 --gateway=172.18.1.1 device_field

# Supervisory Network (SCADA, HMI)
docker network create --subnet=172.18.2.0/24 --gateway=172.18.2.1 supervisory_field

# DMZ
docker network create --subnet=172.18.3.0/24 --gateway=172.18.3.1 dmz

# IT Department Network
docker network create --subnet=172.18.4.0/24 --gateway=172.18.4.1 it_depart

echo "All subnets created."
```

##  Router Containers with IPTABLES

Each subnet is connected to a dedicated router container (e.g. router_1, router_2) which:

- Is attached to two networks (e.g. device_field and supervisory_field)
- Forwards traffic between subnets
- Enforces firewall rules using `iptables`

**Example:** router_1 (device_field and supervisory_field)

```
# Start router_1 on the main network (or one of the zones)
docker run -d --name router_1 --net scada_network  --ip 172.18.0.2 --privileged --cap-add=NET_ADMIN ubuntu:latest
# Connect router_1 to the Device Field and Supervisory subnets
docker network connect device_field router_1
docker network connect supervisory_field router_1
```

- With this example, you could do same for other networks

## Container Attachment Example

```bash
#!/bin/bash
(
cd "OpenPLC_v3_customized" || exit 1

# check if running as root
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

# build and run the plcs
for i in {11..16}
do
  sudo docker build -t plc"$i":oplcv3 .
  sudo docker run --net device_field --ip 172.18.0."$i" -d  --privileged --name plc"$i" -p 100"$i":8080 plc"$i":oplcv3
done


)


# build and run scadaBR
(
cd scadabr || exit 1
sudo docker build -t scadabr:scadabr .
sudo docker run --net supervisory_field --ip 172.18.0.9 -d --privileged --name HMI-HIS -p 10010:8080 scadabr:scadabr
)



#  build and run the simulator
(
cd sim || exit 1
sudo docker build -t sim:sim .
sudo docker run --net device_field --ip 172.18.0.10 -d --privileged --name MTU -h MTU sim:sim
)
```

## This really makes configuration flexible

