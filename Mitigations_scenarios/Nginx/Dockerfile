# # nginx/Dockerfile
# FROM nginx:alpine

# # Copy custom Nginx config
# COPY nginx.conf /etc/nginx/nginx.conf

# # Copy SSL certificates (generate them first or use Let's Encrypt)
# COPY certs/ /etc/nginx/certs/

# # Expose HTTPS port
# EXPOSE 443

# # Start Nginx
# CMD ["nginx", "-g", "daemon off;"]

FROM nginx:alpine
COPY nginx.conf  /etc/nginx/conf.d/default.conf
COPY certs /etc/nginx/certs
