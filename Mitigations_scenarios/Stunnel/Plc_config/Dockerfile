FROM debian:bullseye
RUN apt update && apt install -y stunnel4
COPY ca-certs.pem /etc/stunnel/ca-certs.pem
COPY plc11-client.conf /etc/stunnel/stunnel.conf
CMD ["stunnel", "/etc/stunnel/stunnel.conf"]
