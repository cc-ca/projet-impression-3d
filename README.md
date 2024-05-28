# PrintGuard: Real-Time Error Detection for 3D Printing

## Overview

PrintGuard  is a device designed to prevent plastic waste during failed 3D prints by using AI and a camera to detect failures.

## 1. How it Works

PrintGuard employs AI with a camera to monitor and detect print failures.

The web-based dashboard (`http://<ip_raspberry>:5000/`) displays useful information.

The State diagram is used to describe the nominal process bellow:

![StateDiagram (2)](https://github.com/cc-ca/projet-impression-3d/assets/65626912/2b9dab5f-703e-4115-92e0-2667a610ceb0)


## 2. Wiring

### Required Components
- 1 USB webcam
- 1 RGB LED
- 1 button
- 4 resistors (220 Ohms)
- 1 Raspberry Pi

![Wiring Diagram](https://github.com/cc-ca/projet-impression-3d/assets/65626912/4fd35d57-26c4-41d8-8104-bdc7c5d9b96c)

## 3. How to Install

### Hardware Installation

1. **Webcam**: Connect the USB webcam to the Raspberry Pi.
2. **LED and Button Wiring**:
    - **RGB LED**:
        - Red: GPIO Pin 19
        - Green: GPIO Pin 13
        - Blue: GPIO Pin 26
    - **Button**:
        - Connect one leg of the button to GPIO Pin 6.
    - **Switch**:
        - Connect the switch to GPIO Pin 4 .
    - **Resistors**: Use 220 Ohm resistors for each connection to the RGB LED and 10 KOhm the button to the ground

### Software Installation
1. **Download Raspbian Lite**: Obtain the latest software package from the [official repository](https://www.raspberrypi.com/software/).
2. **Install Git (optional)**:
   ```bash
   sudo apt-get install git git-lfs
3. **Clone the GitLab Repository**:
   ```bash
   git clone https://github.com/cc-ca/projet-impression-3d.git
4. **Run Setup**:
   ```bash
   cd projet-impression-3d
   make setup
5. **Reboot the Raspberry Pi**:
   ```bash
   sudo reboot
For more information, visit [the GitHub repository](https://github.com/cc-ca/projet-impression-3d).
