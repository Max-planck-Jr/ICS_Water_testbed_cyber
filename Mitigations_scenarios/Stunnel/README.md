# Secure Modbus TCP Communication with Stunnel in Docker for ScadaBR

This guide shows you how to **secure Modbus TCP connections** between PLCs and a ScadaBR instance using **`stunnel`** in the ICS *testbed*. `stunnel` encrypts traffic using TLS, making insecure protocols like Modbus TCP safe to use across containerized networks.

## Components 

- `stunnel-server` (TLS decryptor at ScadaBR side)
- `stunnel-client-plcX` (TLS encryptor on each PLC side)
- ScadaBR (unmodified)
- One or more Modbus TCP-based PLC containers

### Use case 

[PLC container] → localhost:1502 → [stunnel-client-plcX] → 🔐TLS→ [stunnel-server] → localhost:502 → [ScadaBR container]

## Why use stunnel 

-  Encrypts insecure protocols like Modbus TCP
- Integrates easily with existing containers
- Lightweight and fast
- Does not require changes to PLC or ScadaBR

## Stunnel structure 

```
Stunnel/
├── README.md 
├── Scadabr_config/
│   ├── Dockerfile
│   ├── scada-server.conf
│   └── stunnel.pem
└── Plc_config/
    ├── Dockerfile
    ├── plc11-client.conf
    └── ca-certs.pem
```

## How to use stunnel in the simulated ICS testbed

We assume that the simulation is already launched. In the host machine : 

- Generate TLS Certificate

bash
```
openssl req -new -x509 -days 365 -nodes -out stunnel.pem -keyout stunnel.pem
```
- Copy stunnel.pem to scada-stunnel/ and copy stunnel.pem to plc11-stunnel/ and rename it ca-certs.pem
- Configure `stunnel-server` for ScadaBR
scada-stunnel/scada-server.conf
```
foreground = yes
debug = 7
cert = /etc/stunnel/stunnel.pem
pid = /tmp/stunnel.pid

[plc1]
accept = 1502
connect = 127.0.0.1:502

# [plc2]
# accept = 1503
# connect = 127.0.0.1:503

# [plc3]
# accept = 1504
# connect = 127.0.0.1:504
```

Scadabr_config/Dockerfile
```
FROM debian:bullseye
RUN apt update && apt install -y stunnel4
COPY stunnel.pem /etc/stunnel/stunnel.pem
COPY scada-server.conf /etc/stunnel/stunnel.conf
CMD ["stunnel", "/etc/stunnel/stunnel.conf"]
```

- Configure `stunnel-client` for PLC

Plc_config/Dockerfile
```
client = yes
foreground = yes
CAfile = /etc/stunnel/ca-certs.pem
debug = 7

[modbus]
accept = 127.0.0.1:1502
connect = 172.18.0.9:1502  # ScadaBR IP
```

Plc_config/Dockerfile
```
FROM debian:bullseye
RUN apt update && apt install -y stunnel4
COPY ca-certs.pem /etc/stunnel/ca-certs.pem
COPY plc11-client.conf /etc/stunnel/stunnel.conf
CMD ["stunnel", "/etc/stunnel/stunnel.conf"]
```

- You can now launch the docker containers in the networks

bash
```
docker build -t stunnel-server .
docker run -d --network swat --ip 172.18.0.3 --name stunnel-server stunnel-server
```

bash
```
docker build -t stunnel-client .
docker run -d --network swat --ip 172.18.0.4 --name stunnel-client stunnel-client
```

*NB:* The stunnel server and clients are assigned to the `swat` network. 

- Verify everything works correctly : 
Inside the plc11 container:

plc11 bash
```
telnet 172.18.0.21 1502
```
It should connect (This is the stunnel-client)

- Check `docker logs stunnel-client` and `stunnel-server` for successful TLS handshake.
- In ScadaBR GUI, add a modbus TCP data source, `Host: 127.0.0.1` and `port:502`
- After testing the connection, we should get values if PLC is working fine

## Flexibility & Scaling

- Add more PLCs by duplicating plcX-stunnel folder with unique ports.
- Each PLC can have its own TLS tunnel.
- Modularity means ScadaBR and PLC containers remain untouched.
