# Setting Up Attack Scenarios


## *ICS Network  network environment*
At this level, we consider you've installed the original testbed network (i.e from Yi Zhu's work). No mitigation solution has been implemented yet so all the components in the swat network can communicate with each other, no isolation nor segmentation is implemented yet.

## *Services running after running testbed*

Docker Containers

**ScadaBR**
   - **Role:** Simulates a HMI and Historian in the Scada Network.
   - **Network:**
     - `Name` (Swat) 
     - `Ip address` (IP: 172.18.0.9)
   - **Ports:** 10010:8080

**PLC11**
   - **Role:** Simulates a PLC via OpenPLC in the Scada Network.
   - **Networks:**
     - `Name` (Swat)
     - `network2` (IP: 172.18.0.11)
   - **Ports:** 10011:8080

**PLC12**
   - **Role:** Simulates a PLC via OpenPLC in the Scada Network.
   - **Networks:**
     - `Name` (Swat)
     - `network2` (IP: 172.18.0.12)
   - **Ports:** 10012:8080


**NB:** There are 06 PLC in total, from PLC11 ... PLC16, there are in the same network named (swat) with their port number correspond to their names 
**Ex :** Name :  PLC11, Port : 10011

## *Setting up the attackers machine*

Docker command:
```
sudo docker run -d -t --net swat --hostname attacker --name attacker --privileged --ip 172.18.0.18 -p 10018:8080 kalilinux/kali-rolling
```

Docker container

**Attacker**
   - **Role:** Simulates the attacker in the Scada network.
   - **Image:** `kalilinux/kali-rolling`
   - **Networks:**
     - `Name` (Swat)
     - `network2` (IP: 172.18.0.18)
   - **Ports:** 10018:8080
   - **Description:** The attacker will install the basic tools to counter attack.

**NB:** We assume the attack is already in the swat network so he can access other components of the Scada network