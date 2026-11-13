# dream-server

Anonymous aggregate server for the "Everyone's dreams" report in the Dream app.

- Stores only keywords, feelings, day, country and optional age band / gender under a random install ID. Never dream text, names, or IP addresses.
- Every figure is computed over at least `DREAM_MIN_PEOPLE` (default 10) different people; smaller groups are withheld.
- `POST /v1/dreams`, `POST /v1/forget`, `GET /v1/summary`, `POST /v1/events` (admin), `GET /health`.
- Admin (header `X-Admin-Token`): `GET /v1/admin/overview`, `GET /v1/admin/export?kind=entries|daily|words|feelings|countries|demographics&from=YYYY-MM-DD&to=YYYY-MM-DD` (CSV). Install IDs are replaced by one-way pseudonyms.
- Update only the server: `sudo curl -fsSL https://raw.githubusercontent.com/YusukeSasamura/dream-server/main/server.py -o /opt/dream-server/server.py && sudo systemctl restart dream-server`

Install on Ubuntu/Debian:

    curl -fsSL https://raw.githubusercontent.com/YusukeSasamura/dream-server/main/install.sh | sudo bash
