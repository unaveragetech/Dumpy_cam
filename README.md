

# Media Stream Controller

The **Media Stream Controller** is a Python-Flask-based web application that allows users to control and monitor live camera feeds. This tool includes functionalities for switching cameras, turning the camera on and off, saving images and GIFs from the live feed, and displaying connection stats. It is designed for ease of use with a simple web interface and real-time updates.

## Features

- **Live Camera Feed**: Displays a real-time camera feed on the web interface.
- **Camera Controls**:
  - Toggle the camera on and off.
  - Switch between multiple connected cameras.
  - Save pictures and GIFs from the live feed.
- **Connection Stats**:
  - Displays the total connection duration.
  - Tracks the total number of pictures taken.
- **Image Gallery**: Displays all saved images, allowing for quick review.
- **Dependency Handling**: The script automatically fetches missing dependencies, installs them, and restarts to ensure proper functionality.
  
## Installation

### Prerequisites

- Python 3.x
- Flask
- OpenCV (`cv2`)
- Additional Python packages (will be auto-installed by the script)

### Step-by-Step Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/media-stream-controller.git
    cd media-stream-controller
    ```

2. **Install dependencies**:
   - All necessary dependencies will be installed automatically when you first run the script.
   - If you want to manually install them, run:
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the application**:
    ```bash
    python app.py
    ```

4. **Access the web interface**:
    - Open your web browser and go to `http://localhost:5000` to access the Media Stream Controller.

## Usage

### Web Interface

- **Live Camera Feed**: The live camera feed is displayed at the top of the page.
- **Control Buttons**:
  - **Turn Camera ON/OFF**: Allows you to toggle the camera feed.
  - **Switch Cameras**: If you have multiple cameras connected, you can switch between them.
  - **Save Picture**: Saves the current frame as a picture in the application’s directory.
  - **Save GIF**: Records a short GIF from the current camera feed.
- **Connection Stats**:
  - **Connection Duration**: Shows how long the current session has been active.
  - **Total Pictures Taken**: Displays how many images have been captured during the session.
- **Image Gallery**: Displays all saved images dynamically as you take pictures.

### API Endpoints

You can control the camera and other features through the following API endpoints:

| Endpoint            | Method | Description                          |
|---------------------|--------|--------------------------------------|
| `/video_feed`       | GET    | Streams the live video feed.         |
| `/toggle/on`        | GET    | Turns the camera on.                 |
| `/toggle/off`       | GET    | Turns the camera off.                |
| `/switch_camera/<id>` | GET    | Switches between connected cameras.  |
| `/save_picture`     | GET    | Captures and saves a picture.        |
| `/save_gif`         | GET    | Captures and saves a short GIF.      |

### Image and GIF Storage

- **Images** are saved as `.jpg` files in the root folder of the project.
- **GIFs** are saved as `.gif` files in the root folder as well.
- The gallery in the web interface will automatically update with each new image captured.

### Dependencies Handling

When the script runs for the first time, it checks for missing dependencies, installs them, and restarts automatically to ensure smooth operation.

### Auto-Restart after Dependency Installation

If the script installs any dependencies, it will automatically restart itself to activate them without manual intervention.

## Project Structure

```bash
├── app.py                # Main Python application
├── templates
│   └── index.html        # Main web interface
├── static
│   └── styles.css        # CSS for the web interface
├── requirements.txt      # List of Python dependencies
├── README.md             # Project documentation
```

## Customization

### Adding More Cameras

To add more cameras, you can modify the camera switching logic in `app.py` to handle multiple connected devices. You can map each camera to an ID and call the `/switch_camera/<id>` endpoint to switch between them.

### Changing File Save Locations

By default, pictures and GIFs are saved in the root project directory. You can change this behavior by modifying the save paths in the `save_picture()` and `save_gif()` functions in `app.py`.

## Example Screenshots-- will add at realease

### Live Camera Feed and Controls

![Live Camera Feed Screenshot](screenshots/camera-feed.png)-- will add at realease

### Image Gallery

![Image Gallery Screenshot](screenshots/image-gallery.png)-- will add at realease

## Contributing

Feel free to submit issues or pull requests to improve the tool. Contributions are welcome!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
