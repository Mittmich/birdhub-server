FROM nginx
COPY nginx.conf /etc/nginx/nginx.conf
# copy password file
COPY .htpasswd /etc/nginx/.htpasswd
# copy certificate
COPY self-signed.crt /etc/nginx/ssl/self-signed.crt
COPY self-signed.key /etc/nginx/ssl/self-signed.key