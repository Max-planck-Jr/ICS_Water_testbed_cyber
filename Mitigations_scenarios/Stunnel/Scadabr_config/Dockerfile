FROM debian:bullseye
RUN apt update && apt install -y stunnel4
COPY stunnel.pem /etc/stunnel/stunnel.pem
COPY scada-server.conf /etc/stunnel/stunnel.conf
CMD ["stunnel", "/etc/stunnel/stunnel.conf"]
