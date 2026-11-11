#!/usr/bin/env bash
# Installs the Dream "Everyone's dreams" server on Ubuntu/Debian.
#   curl -fsSL https://raw.githubusercontent.com/YusukeSasamura/dream-server/main/install.sh | sudo bash
# Re-running updates the server and keeps the data and the admin token.
set -euo pipefail
[ "$(id -u)" = 0 ] || { echo "run with sudo"; exit 1; }
REPO=https://raw.githubusercontent.com/YusukeSasamura/dream-server/main
export DEBIAN_FRONTEND=noninteractive

apt-get update -qq
apt-get install -y -qq python3 curl ca-certificates sqlite3 >/dev/null

id dream >/dev/null 2>&1 || useradd --system --home /var/lib/dream-server --shell /usr/sbin/nologin dream
install -d -o dream -g dream -m 700 /var/lib/dream-server
install -d -m 755 /opt/dream-server /etc/dream-server
curl -fsSL "$REPO/server.py" -o /opt/dream-server/server.py

if [ ! -f /etc/dream-server/env ]; then
  echo "DREAM_ADMIN_TOKEN=$(head -c 24 /dev/urandom | od -An -tx1 | tr -d ' \n')" > /etc/dream-server/env
  echo "DREAM_MIN_PEOPLE=10" >> /etc/dream-server/env
  chmod 600 /etc/dream-server/env
fi

cat > /etc/systemd/system/dream-server.service <<UNIT
[Unit]
Description=Dream everyone's-dreams server
After=network.target
[Service]
User=dream
EnvironmentFile=/etc/dream-server/env
ExecStart=/usr/bin/python3 /opt/dream-server/server.py
Restart=always
NoNewPrivileges=true
ProtectSystem=strict
ReadWritePaths=/var/lib/dream-server
[Install]
WantedBy=multi-user.target
UNIT
systemctl daemon-reload
systemctl enable --now dream-server >/dev/null
systemctl restart dream-server

# Public name: DREAM_HOST if given, otherwise <ip>.sslip.io (free DNS that points at this server).
IP=$(curl -fsS4 https://api.ipify.org || hostname -I | awk '{print $1}')
HOST=${DREAM_HOST:-$(echo "$IP" | tr . -).sslip.io}

if command -v nginx >/dev/null 2>&1 && systemctl is-active --quiet nginx; then
  # nginx already serves this machine: add a site for Dream and get a certificate with certbot.
  apt-get install -y -qq certbot python3-certbot-nginx >/dev/null
  cat > /etc/nginx/sites-available/dream-server <<NGX
server {
  listen 80;
  server_name $HOST;
  location / { proxy_pass http://127.0.0.1:8787; proxy_set_header X-Forwarded-For \$remote_addr; client_max_body_size 16k; }
}
NGX
  ln -sf /etc/nginx/sites-available/dream-server /etc/nginx/sites-enabled/dream-server
  nginx -t && systemctl reload nginx
  certbot --nginx -d "$HOST" --non-interactive --agree-tos --register-unsafely-without-email --redirect || echo "!! certbot failed: open ports 80 and 443"
else
  # Otherwise use Caddy, which gets and renews the certificate by itself.
  if ! command -v caddy >/dev/null 2>&1; then
    apt-get install -y -qq debian-keyring debian-archive-keyring apt-transport-https gnupg >/dev/null
    curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | gpg --dearmor --yes -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
    curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' > /etc/apt/sources.list.d/caddy-stable.list
    apt-get update -qq && apt-get install -y -qq caddy >/dev/null
  fi
  if ! grep -q "dream-server" /etc/caddy/Caddyfile 2>/dev/null || ! grep -q "$HOST" /etc/caddy/Caddyfile; then
    cat > /etc/caddy/Caddyfile <<CADDY
# dream-server
$HOST {
  request_body { max_size 16KB }
  reverse_proxy 127.0.0.1:8787
  log { output discard }
}
CADDY
  fi
  systemctl enable --now caddy >/dev/null
  systemctl reload caddy || systemctl restart caddy
fi

command -v ufw >/dev/null 2>&1 && ufw status | grep -q active && { ufw allow 80/tcp; ufw allow 443/tcp; } >/dev/null || true

sleep 3
echo
echo "===================================================="
echo " Dream server is running."
echo " URL:   https://$HOST"
echo " Check: curl https://$HOST/health"
echo " Admin token: sudo cat /etc/dream-server/env"
echo "===================================================="
curl -fsS "http://127.0.0.1:8787/health" && echo
