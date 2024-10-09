# E-paper ESP32 Frame

![ESP e-paper frame](images/e-paper-esp32-frame.jpg?raw=true)
![ESP e-paper frame](images/e-paper-esp32-frame-backside.jpg?raw=true)

This project provides a comprehensive installation guide for an e-paper picture frame that updates daily. The frame features a Waveshare seven-color e-paper display, which, combined with the implemented Floyd-Steinberg Dithering algorithm, creates the illusion of a greater color depth. Users have the ability to convert their own images using the included BMP-Converter. Additionally, the frame can be connected to the internet to display specific images on designated days. The 1000mAh battery is expected to last for approximately 700 days and can be recharged through the ESP32's type-C port.

## Features

- **Daily Updates**: Automatically updates the displayed image daily.
- **Internet Connectivity**: Connects to the internet to fetch images based on specific dates.
- **Image Conversion**: Includes a BMP-Converter for converting images to the required format.
- **Low Power Consumption**: Utilizes the FireBeetle 2 ESP32-E for low power consumption during deep sleep.
- **Customizable**: Users can convert and display their own images.
- **3D Printed Case**: Provides a 3D printed case design for housing all components

## Table of Contents

- [Components](#components)
- [Installation](#installation)
- [Convert the images](#convert-the-images)
- [Contributing](#contributing)
- [License](#license)

## Components

- FireBeetle 2 ESP32-E: A microcontroller with low power consumption during deep sleep.
- Li-Po 503450 1000mAh 3.7V with PH2.0 connector: A rechargeable lithium polymer battery for power supply. (Dimensions: 5mm (H) x 34mm (W) x 50mm (L))
- Micro SD Card Module: A module for handling micro SD cards. (Dimensions: 18mm x 18mm)
- Waveshare 7.3inch ACeP 7-Color E-Paper E-Ink Display Module + HAT: An e-paper display module with seven colors, SPI communication, featuring 800×480 pixels.
- Toggle Switch (Optional): A switch used to turn off the power from the battery. (Thread diameter: 5mm)
- Printed Case: A 3D printed case to hold all the components.
- Four Heat Inserts and Screws: Hardware components for assembly. (M3)
- Picture frame: A standard picture frame that can accommodate the e-paper frame.


## Installation

1. Clone the repository:
	```sh
	git clone https://github.com/Duocervisia/e-paper-esp32-frame.git
	```
3. Connect your ESP32 to the e-paper display and SD card module according to the `Schematic for Components.png`. Cut the low-power Solder Jumper Pad, located on the front side of the Firebeetle 2, to achieve optimal power consumption during deep sleep.
4. Upload the code to your ESP32.
5. Convert the images you want to display using the BMP-Converter. See [Convert the images](#convert-the-images). This application can convert most image formats to BMP format with the correct dimensions of 800 x 480 px, which is needed for the microcontroller to display the image. It also provides basic operations to modify the images.
6. Add the converted images to the SD card, including the info.txt file.
7. (Optional) Copy the setup.json file to the SD card and set the SSID and password in the file. This allows the ESP32 to connect to the internet. The current date will be pulled from an ntp server, to update the image based on the date specified in the filename using the BMP-Converter. With internet connectivity, the ESP32 will update the image at approximately 10 o'clock. Without internet, the ESP32 will sleep for 24 hours (based on the internal clock) and update the image based on name sorting.
8. Print the case using a 3D printer.
9. (Optional) Create a small hole, for example using a soldering iron, between the battery and ESP32 to integrate a toggle switch.
10. Attach the 3D printed case to the backplate of the picture frame by creating a small slit on the top. You can either glue the case to the backplate or use screws to secure them together. On the opposite side, mount the e-paper display. Connect the ribbon cable of the e-paper to the case through the created slit. For a perfect fit, use the provided `passepartout.pdf` file.

## Convert the images

To convert the images, follow these steps:

1. Navigate to the `/bmpConverter/build` directory.
2. Run the `converter.exe` executable.

Alternatively, you can follow these steps:

1. Navigate to the `/bmpConverter` directory.
2. Read the `README` file in the directory and install the required dependencies.
3. Run the `converter.py` script.

## Contributing

Contributions are highly appreciated! Feel free to open an issue or submit a pull request. A big thank you to TreeSparrow69 for their valuable contributions to this project.

## License

This project is licensed under the MIT License.
