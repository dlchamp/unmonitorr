# Unmonitorr

Unmonitorr is a lightweight tool designed to listen for incoming webhook notifications from Radarr and Sonarr, enabling automated management of media. Depending on your configuration, Unmonitorr can either unmonitor or remove media directly from Radarr and Sonarr.

Built with Python 3.12 and `aiohttp`, Unmonitorr is fully asynchronous and optimized for efficiency.

---

## Features
- Listens for Radarr and Sonarr webhook notifications.
- Automatically unmonitor episodes or series.
- Optionally removes media from Radarr and Sonarr based on user configuration.

---

## How It Works
1. Unmonitorr runs a small web server using `aiohttp`.
2. It receives webhook notifications from Radarr and Sonarr.
3. Depending on your configuration:
   - Unmonitorr unmonitors the media (episodes, movies, or series).
   - Optionally removes the media from Radarr or Sonarr.
4. It uses the respective APIs to perform these operations.

---

## Requirements
- Python 3.12+
- Radarr and/or Sonarr configured to send webhooks to Unmonitorr.
- aiohttp
- Docker (optional, for containerized deployments).
---

## Installation

### Configuration Options
Unmonitorr can be configured by visiting `/setup`
(ex. http://localhost:8080/setup)

---

### Setting Up with Docker

#### Using `docker run`
1. Pull the image: `docker pull ghcr.io/dlchamp/unmonitorr:latest` or you may build it yourself:
    ```bash
    docker build -t unmonitorr:latest .
    ```

2. Run the container, passing in environment variables:
    ```bash
    docker run -d \
        --name unmonitorr \
        -p 8080:8080 \
        -e LOG_LEVEL=info \
        ghcr.io/dlchamp/unmonitorr:latest
    ```

#### Using `docker-compose`
1. Create a `docker-compose.yml` file:
    ```yaml
    version: "3.9"
    services:
      unmonitorr:
        image: ghcr.io/dlchamp/unmonitorr:latest
        container_name: unmonitorr
        ports:
          - "8080:8080"
        environment:
          LOG_LEVEL: "info"
    ```

2. Run the container:
    ```bash
    docker-compose up -d
    ```

3. Verify the server is running:
    ```bash
    docker logs unmonitorr
    ```

---

## Configuring Webhooks in Radarr and Sonarr
1. Open Radarr or Sonarr.
2. Navigate to **Settings** > **Connect**.
3. Click the **+** button to add a new connection.
4. Scroll down and select **Webhook**.
5. Give the connection a name.
6. Select the desired trigger (On Grab or On File Import).
7. Add tags if you want to handle specific media.
8. Add the webhook URL:
   - Use the host and port where Unmonitorr is running (e.g., `http://<your-ip>:8080/radarr` or `http://<your-ip>:8080/sonarr`).
9. Click **Test**.
   - If successful, you will see a green checkmark in Radarr/Sonarr and a test log in Unmonitorr.
10. Save the webhook connection.

---


## License
Unmonitorr is licensed under the MIT License.

---

## Contributing
Contributions are welcome! Please submit a pull request or open an issue to discuss your ideas.

---

## Issues
If you encounter any problems or have questions, please open an issue on the [GitHub repository](https://github.com/dlchamp/unmonitorr/issues).
