<!-- References -->
[requirements-url]: https://github.com/cc-ca/projet-impression-3d/blob/main/requirements.txt "Project requirements"



# PrintGuard
Real-Time Error Detection for 3D Printing

![PrintGuard Device on operation](https://github.com/cc-ca/projet-impression-3d/blob/main/.github/images/the_system_in_operation.jpg)

![PrintGuard Web Interface](https://github.com/cc-ca/projet-impression-3d/blob/main/.github/images/webinterface.png)

PrintGuard is a device designed to prevent plastic waste from failed 3D prints by using artificial intelligence and a camera to detect failures during printing.

It uses a raspberry Pi as a working device, combined with a camera and a relay (electrically operated switch) to collect and stop any 3D printer (Prusa, Ultimaker or others).

Via a web interface on your local network, you can view and manage the product in real time.
Ideal for positioning your camera correctly, managing the relay trigger threshold or remotely shutting down your 3d printer.



## Table of contents

- [Requirements](#requirements)
    - [Libraries](#libraries)
    - [Components](#components)
- [Installing](#installing)
    - [Hardware Installation](#hardware-installation)
    - [Software Installation](#software-installation)
- [Usage](#usage)


## Requirements

### Libraries

- [Python](https://www.python.org/) == 3.9 (Has not been tested for more recent versions)
- [RPi.GPIO](https://pypi.org/project/RPi.GPIO/) >= 0.7.1 : A module to control Raspberry Pi GPIO channels
- [tensorflow](https://www.tensorflow.org/) == 2.16.1 :  Python interface for machine learning and artificial intelligence.
- [opencv-python-headless](https://opencv.org/) >= 4.9.0.80 : Open Computer Vision Library
- [Flask](https://flask.palletsprojects.com/) >= 3.0.3 : Micro web framework written in Python

The complete list is in [requirements.txt][requirements-url]

### Components

- 1 Raspberry Pi
- 1 230V Power Relays
- 1 USB webcam (preferably with autofocus)
- 1 RGB LED
- 1 button
- 3 resistors of 220 Ohms and 1 of 1 kOhm
- Some electrical wires
- a fan (if the system is in a box)


## Install

### Hardware Installation

Connect the components as shown below:

![Electronic circuit](https://github.com/cc-ca/projet-impression-3d/blob/main/.github/images/electronic_circuit.png)


- **RGB LED**:
    - Red: GPIO Pin 19
    - Green: GPIO Pin 13
    - Blue: GPIO Pin 26
    - A 220 Ohm resistor between each GPIO and each RGB pin
- **Button**:
    - One leg to GPIO Pin 6
    - The other leg to the ground by a 1 kOhm resistor.
- **Relay**:
    - GPIO Pin 4 .

### Software Installation

1. **Install Raspbian or any other Debian-based operating system**:

We recommend using the [Raspberry Pi Imager](https://www.raspberrypi.com/software/) provided by the official Raspberry project to easily create a bootable SD card for your Raspberry.
You need to be able to connect to the operating system to perform the following installation steps (for example, via ssh on your local network)

2. **Install Git and clone the repository**:

Connect to your raspberry with an administrator account and clone the repository in your personal directory:

```bash
sudo apt install git
git clone https://github.com/cc-ca/projet-impression-3d.git
```

4. **Make Setup**:

Go to the repository directory and start the setup script:

```bash
cd projet-impression-3d
make setup
```

This installs all the necessary dependencies in a virtual environment and creates a systemd service to start the program automatically when the raspberry pi is booted.
You will be asked for your user password and to accept the installation of the missing dependencies.

5. **First launch of the programme**:

You can start the program immediately using the systemd service or the `make run` option (developer-oriented) :
```bash
# Using Systemd service
sudo systemctl start 3dprinter_error_detector.service
systemctl status 3dprinter_error_detector.service
```
Or
```bash
# Using Makefile
make run
```

Otherwise the program will run automatically the next time the raspberry pi is started.

```bash
sudo systemctl reboot # or poweroff
```

If you do not want this behaviour, simply disable it with this command.

```bash
sudo systemctl disable 3dprinter_error_detector.service
systemctl status 3dprinter_error_detector.service
```



## Usage

The system is operated using the button, and the situation is indicated by a colour code on the RGB LED :
 - Blue indicates that the system is waiting for the user (paused).
 - Yellow indicates a problem. (The camera is probably not connected properly)
 - Green or Red indicates that the system is running and returns the last prediction made by the machine learning model (green = OK, red = an error has been detected).

You can refer to the diagram below to understand all the interactions:

![State-transition diagram](https://github.com/cc-ca/projet-impression-3d/blob/main/.github/images/state-transition_diagram.png)


We also provide a web interface available at this address [http://<ip_raspberry>:5000/](http://<ip_raspberry>:5000/) to get image feedback from the camera (useful for positioning it), modify the trigger threshold and perform an emergency stop.