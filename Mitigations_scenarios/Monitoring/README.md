# Monitoring SCADA Network with Grafana Loki + Promtail

This guide shows how to set up **Loki**, **Promtail**, and **Grafana** to monitor logs from our **ICS testbed** including PLCs, ScadaBR, and Stunnel sidecars with minimal effort.

## Components

- *Grafana Loki:* Log aggregation system
- *Promtail:* Log collector and shipper
- *Grafana:* Dashboard for visualizing logs
- *Docker logging driver:* Directs container logs to Loki

## Network Assumptions

You have a custom Docker network (e.g. `swat`) already used by your SCADA and PLC containers.

```bash
docker network ls
```
## Simple and flexible installation 

- Download Loki and Promtail Configs

```bash
wget https://raw.githubusercontent.com/grafana/loki/v3.4.1/cmd/loki/loki-local-config.yaml -O loki-config.yaml
wget https://raw.githubusercontent.com/grafana/loki/v3.4.1/clients/cmd/promtail/promtail-docker-config.yaml -O promtail-config.yaml
```

- Run Loki, Promtail & Grafana Containers

Loki
```bash
docker run --name loki -h loki --net swat --ip 172.18.0.21 --privileged -d -v $(pwd):/mnt/config -p 3100:3100 grafana/loki:3.4.1 -config.file=/mnt/config/loki-config.yaml
```

Promtail
```bash
docker run --name promtail -h promtail --net swat --ip 172.18.0.22 --privileged -d -v $(pwd):/mnt/config -v /var/log:/var/log --link loki grafana/promtail:3.4.1 -config.file=/mnt/config/promtail-config.yaml
```

Grafana
```bash
docker run --name grafana -h grafana --net swat --ip 172.18.0.23 --privileged -d -p 3000:3000 --link loki grafana/grafana
```

- Install Docker Loki Logging Driver 

```bash
docker plugin install grafana/loki-docker-driver:latest --alias loki --grant-all-permissions
```

- Configure Docker to Use Loki Driver

Edit or create /etc/docker/daemon.json:
```json
{
  "debug": true,
  "log-driver": "loki",
  "log-opts": {
    "loki-url": "http://172.18.0.21:3100/loki/api/v1/push",
    "loki-batch-size": "400"
  }
}
```

-  Restart Docker for changes to apply:

```bash
sudo systemctl restart docker
```

### Recreate All Other Containers

Since logging must start with container creation, you must recreate your SCADA-related containers (ScadaBR, PLCs, stunnel clients/servers) after the driver is active. 

## Access Grafana Dashboard

- Open Grafana: http://localhost:3000
- You can sign up 
- Add a Loki Data Source: 
- Create a dashboard or explore logs from various containers.

### Benefits

-  Real-time visibility into SCADA components
-  Centralized logging (including stunnel, PLC, and SCADA logs)
- Security and observability combined
-  Minimal configuration with flexible expansion


