# Create Router 1 container
docker run -d --name router_field_supervisory --cap-add=NET_ADMIN --cap-add=SYS_MODULE --network field_device --ip 172.18.1.254 alpine:latest sh -c "apk add iptables && tail -f /dev/null"

# Connect to supervisory network
docker network connect --ip 172.18.2.254 supervisory router_field_supervisory


# Create Router 2 container  
docker run -d --name router_supervisory_dmz --cap-add=NET_ADMIN --cap-add=SYS_MODULE --network supervisory --ip 172.18.2.253 alpine:latest sh -c "apk add iptables && tail -f /dev/null"

# Connect to DMZ network
docker network connect --ip 172.18.3.254 dmz router_supervisory_dmz


# Create Router 3 container
docker run -d --name router_dmz_corporate --cap-add=NET_ADMIN --cap-add=SYS_MODULE --network dmz --ip 172.18.3.253 alpine:latest sh -c "apk add iptables && tail -f /dev/null"

# Connect to corporate network
docker network connect --ip 172.18.4.254 corporate router_dmz_corporate