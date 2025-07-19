# Moduleo

### Introduction
In short, Moduleo is a robot. One that can do a handful of tasks, enabled by its modular design. It's based on a powertrain system with a dual motor driving scheme and a rechargeable Lithium-ion battery. The powertrain platform is be self-contained, with ports to mount different modules upon for flexible configurations. The first module being designed for it is a system of sensors to detect air quality and report it to a mobile app on a user’s device. Other modules may be designed, and need only implement a standard interface of communication to connect to the powertrain platform. The design is ongoing and will be subject to change as different components and technologies are weighed.


### Motivations
The motivations for designing and architecting this project stem from various factors. Firstly, my final embedded systems course, EECS 473, had a pesky requirement that all projects be “useful” and “marketable” rather than simply being fun to make. This project is more an exploration of the technologies in modern embedded systems, that incorporates all I learned in school as well as the analog hardware design I've learned during my tenure as an engineer -- in a fun package.

Secondly, it's my first solo project, building on my software and hardware knowledge while also serving as an exercise in design, manufacturing, and packaging with a bit of CAD and hands on crafting.


<img src="img/earlySketch.png" alt="drawing" width="600"/>


### Block Diagram
<img src="img/blockDiagram.png" alt="drawing" width="800"/>

### Major Themes

I wanted to make a robot (originally inspired by Star Wars Droids)
- I gave myself specific constraints
    - Needed to use my own designed PCB as the central hub of system
    - Needed to use DriverLib or HAL software, minimize Arduino
    - Needed to be network of boards, with UART/I2C connections between them
    - I (eventually) want to incorporate an RTOS


### Project History and progress so far

#### Picking the chassis

I found some spare parts as mechanical basis
Right - old MakeBlock kit Tank Chassis
Left - Tank Chassis from Amazon (for next version)


#### Picking the brains

I knew I needed PWM output for 2-4 motors, I2C drivers for future modules, UART for connecting 2+ MCUs together, and GPIO for LED output, debug, etc.
STM32 was mature platform with good peripherals and DriverLib
Designed around STM32F Dev board

#### Picking a communications platform

Wi-Fi chip was also needed for my preferred communication (Wi-Fi sockets)
Easy choice in hobbyist world - Espressif has best drivers, can use Arduino IDE
Designed around ESP8266 Dev board

#### Picking the batteries
Battery #1: 14.4V rechargeable battery from Shark Robot Vacuum
Battery #2: 2.7V rechargeable battery from Amazon RC car

#### Motor Drivers

Chassis came with 12V brushed motors
Had worked with Brushed motor drivers for a while, had a part in mind
Needed 3.3V VREF and 12V VM

#### How to power it all?

Now we had 2 dev boards, 2 motors, and 2 potential battery voltages
How do I make power tree to work with all the different parts?

- Used a boost and a buck-boost to receive VIN that could be 2-15V

- Used boost to power motors (wanted high voltage, low current)

- Used buck-boost to generate 7.5V rail, LDO to produce 3.3V for logic


<img src="img/powerTree.png" alt="drawing" width="400"/>

<img src="img/fullsetup.jpeg" alt="drawing" width="300"/>


<img src="img/phoneUI.PNG" alt="drawing" width="300"/>


<img src="img/prettySetup.jpeg" alt="drawing" width="300"/>


<img src="img/layout_moduleo.png" alt="drawing" width="300"/>

<img src="img/buckboostPortion.jpeg" alt="drawing" width="300"/>




