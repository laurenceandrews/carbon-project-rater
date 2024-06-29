#!/bin/sh

# Substitute environment variables in the template
envsubst '\$API_URL' < /etc/nginx/templates/default.conf.template > /etc/nginx/conf.d/default.conf

# Output the final nginx configuration for debugging
cat /etc/nginx/conf.d/default.conf

# Start Nginx
nginx -g 'daemon off;'
