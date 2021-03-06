# Fish-Feeder
Set up a hydroponic garden / fish tank installation using a hardware and the internet of things to automate monitoring or maintaining of the system.

# Problem Statement:
For our team project, the group was tasked to set up a hydroponic garden / fish tank installation using hardware and the internet of things to automate monitoring or maintaining of the system.  We have decided to automate feeding of the fish to allow remote feeding when access to the tank installation is not available.   Using Python, the group has interacted with an Arduino to remotely initialize dispensing fish food into the tank and output the status back to a ThingSpeak channel whether or not the feeding was successful.  Additionally, our Feeder apparatus will use a photocell to determine if food remains available for the feed to continue to dispense.  If the photocell detects that the feeder is empty, the system reports that status to ThingSpeak and the dispense food requests is alerted to the status.





## Hardware Setup
### Bill of Materials

|component|vendor|
|---|---|
|Arduino|[SparkFun RedBoard - Programmed with Arduino](https://www.sparkfun.com/products/13975)|
|Breadboard|[Connect Circuit	Breadboard - Self-Adhesive](https://www.sparkfun.com/products/12002)|
|Base|[Hold Boards	Arduino and Breadboard Holder](https://www.sparkfun.com/products/11235)|
|USB Cable|[Connect to Computer	SparkFun USB Mini-B Cable - 6 Foot](https://www.sparkfun.com/products/11301)|
|Jumper Wires|[Circuit Connections	Jumper Wires Standard 7" M/M - 30 AWG (30 Pack)](https://www.sparkfun.com/products/11026)|
|Stepper|[Motor	Drive Feeder	Stepper Motor with Cable](https://www.sparkfun.com/products/938)|
|Motor Driver|[Control Motor	EasyDriver - Stepper Motor Driver](https://www.sparkfun.com/products/12779)|
|Photocell	Light|[Sensor	Mini Photocell](https://www.sparkfun.com/products/9088)|
|Green LED|[Ready Indicator	LED - Basic Green 5mm](https://www.sparkfun.com/products/9592)|
|Yellow LED|[	Run Indicator	LED - Basic Yellow 5mm	](https://www.sparkfun.com/products/9594)|
|Red LED|[Error Indicator	LED - Basic Red 5mm	](https://www.sparkfun.com/products/9590)|
|3 x 330 Ω Resistor|[	Limit Current	Resistor 330 Ω 1/6th Watt PTH](https://www.sparkfun.com/products/8377)|
|1 x 10k Ω Resistor|[	Divide Voltage	Resistor 10k Ω 1/6th Watt PTH](https://www.sparkfun.com/products/8374)|

## Cad prototypes
Here are the cad prototypes designed for the project

The [Body1.stl](Body1.stl) AUTOCAD

The [Body2.stl](Body2.stl) AUTOCAD

The [Body3.stl](Body3.stl) AUTOCAD

The [Body8.stl](Body8.stl) AUTOCAD

The [Body9.stl](Body9.stl) AUTOCAD

The [Body16.stl](Body16.stl) AUTOCAD

## Cad Prototypes after being printed
![docs](https://github.com/BlessingYumbe/Fish-Feeder/blob/master/docs/image2.jpeg)
![docs](https://github.com/BlessingYumbe/Fish-Feeder/blob/master/docs/image4.jpeg)
![docs](https://github.com/BlessingYumbe/Fish-Feeder/blob/master/docs/image7.jpeg)




### Fritzing Diagram
![docs](https://github.com/mapo243/Fish-Feeder/blob/master/docs/Fish%20Feeder.png)

## Connected Hardware

Arduino is connected to the computer via a mini-USB 


![docs](https://github.com/mapo243/Fish-Feeder/blob/master/docs/Circuit%20Photo%203%20Small.png)

## Arduino Code
The [fish_feeder.ino](fish_feeder.ino) sketch was uploaded on the Arduino using the Arduino IDE.

## Python Code

The [fish_feerder.py](fish_feerder.py) script was run in python.

## Results

Screenshot from ThingSpeak Channel showing resulting status updates when fish are fed.

![docs](https://github.com/mapo243/Fish-Feeder/blob/master/docs/Results%20-%20Thingspeak%20Status.png)

## Future Work
This project was quite interesting to set up with the hydroponic fish garden. While using Python, the program was taking time initialize the code itself to prevent multiple ThingSpeak write requests in too short of a time. For future work, another group improve the communication scheme to reduce this delay and prevent failed requests to dispense food.  Additionally, another group could add hardware that can monitor and control conditions such as temperature, lighting, water flow/waste inside the fish garden. And all of these could be fully automated and controlled remotely using a smartphone.
 

## License
The MIT License Copyright <2019><Team Fish Food>
