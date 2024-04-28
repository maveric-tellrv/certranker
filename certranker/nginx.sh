
#!/bin/bash

# Define the content of the nginx.conf file

# Get the hostname dynamically
hostname=$(hostname)

# Replace any value in DNS.1 with the hostname in the OpenSSL configuration file
sed -i "s/DNS.1\s*=\s*.*/DNS.1 = $hostname/g" "openssl.conf"

yum install nginx -y 
mkdir -p /etc/nginx/certs/
openssl genrsa -out /etc/nginx/certs/testranker.key 2048
openssl req -new -key /etc/nginx/certs/testranker.key -out /etc/nginx/certs/testranker.csr  -config openssl.conf
openssl x509 -req -days 365 -in /etc/nginx/certs/testranker.csr -signkey /etc/nginx/certs/testranker.key -out /etc/nginx/certs/testranker.crt


conf_content=$(cat <<EOF

events {
    # Default event processing parameters can be placed here
}

http {
    # HTTP server configurations go here
    server {
        listen 80;
        server_name $hostname;
        return 301 https://\$server_name\$request_uri;
    }

    server {
        listen 443 ssl;
        server_name rovyas.com;
        access_log  /var/log/nginx/example.log;
        ssl_certificate /etc/nginx/certs/testranker.crt;
        ssl_certificate_key /etc/nginx/certs/testranker.key;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_prefer_server_ciphers on;

        location / {
            proxy_pass http://127.0.0.1:8000;
            proxy_set_header Host \$host;
            proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        }
    }
}
EOF
)

# Write the content to the nginx.conf file
echo "$conf_content" > /etc/nginx/nginx.conf
nginx -t

echo "nginx.conf file created successfully."



setsebool -P httpd_can_network_connect 1

systemctl start nginx
