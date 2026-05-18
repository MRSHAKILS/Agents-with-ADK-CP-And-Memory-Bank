FROM nginx:alpine

# Copy index.html
COPY index.html /usr/share/nginx/html/index.template.html

# Expose port 80
EXPOSE 80

# Use envsubst to replace BACKEND_URL in the HTML template and start Nginx
CMD ["/bin/sh", "-c", "envsubst '${BACKEND_URL}' < /usr/share/nginx/html/index.template.html > /usr/share/nginx/html/index.html && nginx -g 'daemon off;'"]
