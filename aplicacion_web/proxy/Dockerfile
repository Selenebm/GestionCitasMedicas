# Dockerfile en proxy/
FROM nginx:alpine

# Copiar configuración personalizada de Nginx
COPY proxy/nginx.conf /etc/nginx/nginx.conf

# Copiar archivos estáticos del frontend desde la API
COPY API/static /usr/share/nginx/html/static
COPY API/templates /usr/share/nginx/html/templates