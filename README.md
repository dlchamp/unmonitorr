# Unmonitorr

Unmonitorr is a lightweight tool designed to listen for incoming webhook notifications from Radarr and Sonarr, enabling automated management of media. Depending on your configuration, Unmonitorr can either unmonitor or remove media directly from Radarr and Sonarr.

Built with Python 3.12 and `aiohttp`, Unmonitorr is fully asynchronous and optimized for efficiency.  
&nbsp;  


## Features
- Listens for Radarr and Sonarr webhook notifications.
- Automatically unmonitor episodes or series.
- Optionally removes media from Radarr and Sonarr based on user configuration.  
&nbsp;  

## How It Works
1. Unmonitorr runs a small web server using `aiohttp`.
2. It receives webhook notifications from Radarr and Sonarr.
3. Depending on your configuration:
   - Unmonitorr unmonitors the media (episodes, movies, or series).
   - Optionally removes the media from Radarr or Sonarr.
4. It uses the respective APIs to perform these operations.  
&nbsp;  

## Requirements
- Python 3.12+
- Radarr and/or Sonarr configured to send webhooks to Unmonitorr.
- aiohttp
- Docker (optional, for containerized deployments).  
&nbsp;  


### Configuration Options
Unmonitorr can be configured by visiting `/setup`
(ex. http://localhost:8080/setup)

![Screenshot of the Config Page](https://github.com/dlchamp/unmonitorr/blob/add-webui-config/config-page.png?raw=true)  
&nbsp;  

# Setting Up with Docker

### Using `docker run`
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
        -v /host/path/unmonitorr/:/app/unmonitorr/data/
        ghcr.io/dlchamp/unmonitorr:latest
    ```  
&nbsp;  

### Using `docker-compose`
1. Create a `docker-compose.yml` file:
    ```yaml
    version: "3.9"
    services:
      unmonitorr:
        image: ghcr.io/dlchamp/unmonitorr:latest
        container_name: unmonitorr
        ports:
          - "8080:8080"
        volumes:
          - /host/path/unmonitorr/:/app/unmonitorr/data/
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
&nbsp;  

### Using Unraid templates
1. Download and save the template in the user templates directory: `wget -O /boot/config/plugins/dockerMan/templates-user/my-unmonitorr.xml https://raw.githubusercontent.com/dlchamp/unraid-templates/main/unmonitorr.xml`
2. Go to the "Docker" tab, scroll down and click "Add Container"
3. At the top: "Select a template" you can click the dropdown, scroll down and click on "unmonitorr"
4. Make any adjustments for default paths, paths, or logging level.
6. Apply changes.
7. Once the container starts, you can right-click and go to the "WebUI" to setup your Sonarr/Radarr API credentials and URLs and adjust the behavior settings.  
&nbsp;  


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
&nbsp;  


## License
Unmonitorr is licensed under the MIT License.  
&nbsp;  


## Contributing
Contributions are welcome! Please submit a pull request or open an issue to discuss your ideas.  
&nbsp;  

## Issues
If you encounter any problems or have questions, please open an issue on the [GitHub repository](https://github.com/dlchamp/unmonitorr/issues).
