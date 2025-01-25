# Unmonitorr

Unmonitorr is a lightweight tool designed to listen for incoming webhook notifications from Radarr and Sonarr, enabling automated management of media. Depending on your configuration, Unmonitorr can either unmonitor or remove media directly from Radarr and Sonarr.

Built with Python 3.12 and `aiohttp`, Unmonitorr is fully asynchronous and optimized for efficiency. 

---

## Features
- Listens for Radarr and Sonarr webhook notifications.
- Automatically unmonitor episodes or series.
- Optionally removes media from Radarr and Sonarr based on user configuration.
- Fully asynchronous for optimal performance.

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
- Docker (optional, for containerized deployments).

---

## Installation

### Configuration Options
These options can be placed into a .env file if using Windows/Linux or you can pass them to your docker run
command or as part of your docker compose if you'd rather do it that way.

| KEY                      | Example Value          | Description                                                                                      |
|---------------------------|------------------------|--------------------------------------------------------------------------------------------------|
| RADARR_PROTOCOL           | http                  | http or https                                                                                   |
| RADARR_HOST               | localhost             | Hostname or IP address for your Radarr instance                                                 |
| RADARR_PORT               | 7878                  | Port used by your instance of Radarr                                                            |
| RADARR_API_KEY            | abc123def456ghi789    | Your API Key (Settings > General > API Key)                                                    |
| SONARR_PROTOCOL           | http                  | http or https                                                                                   |
| SONARR_HOST               | localhost             | Hostname or IP address for your Sonarr instance                                                 |
| SONARR_PORT               | 8989                  | Port used by your instance of Sonarr                                                            |
| SONARR_API_KEY            | xyz987uvw654rst321    | Your API Key (Settings > General > API Key)                                                    |
| HANDLE_EPISODES           | true                  | Automatically unmonitor episodes. Options: true, false                                          |
| HANDLE_SERIES             | true                  | Automatically handle entire series. Options: true, false                                        |
| EXCLUDE_SERIES            | true                  | Add series to import exclusion list. Only applies if REMOVE_MEDIA=true. Options: true, false   |
| HANDLE_SERIES_ENDED_ONLY  | false                 | Only handle series if they are ended and complete. Options: true, false                         |
| REMOVE_MEDIA              | false                 | Remove media from Radarr/Sonarr instead of just "Unmonitor". Options: true, false              |
| LOG_LEVEL                 | info                  | Logging level. Options: debug, info, warning, error, critical                                   |

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
        -e RADARR_PROTOCOL=https \
        -e RADARR_HOST=localhost \
        -e RADARR_PORT=7878 \
        -e RADARR_API_KEY=your_radarr_api_key \
        -e SONARR_PROTOCOL=https \
        -e SONARR_HOST=localhost \
        -e SONARR_PORT=8989 \
        -e SONARR_API_KEY=your_sonarr_api_key \
        -e HANDLE_EPISODES=true \
        -e HANDLE_SERIES=true \
        -e REMOVE_MEDIA=false \
        -e LOG_LEVEL=info \
        unmonitorr
    ```

#### Using `docker-compose`
1. Create a `docker-compose.yml` file:
    ```yaml
    version: "3.9"
    services:
      unmonitorr:
        build: .
        container_name: unmonitorr
        ports:
          - "8080:8080"
        environment:
          RADARR_PROTOCOL: "https"
          RADARR_HOST: "localhost"
          RADARR_PORT: "7878"
          RADARR_API_KEY: "your_radarr_api_key"
          SONARR_PROTOCOL: "https"
          SONARR_HOST: "localhost"
          SONARR_PORT: "8989"
          SONARR_API_KEY: "your_sonarr_api_key"
          HANDLE_EPISODES: "true"
          HANDLE_SERIES: "true"
          REMOVE_MEDIA: "false"
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
