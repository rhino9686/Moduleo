# Moduleo

### Introduction
In short, Moduleo is a small remote-controlled vehicle. One that can do a handful of tasks, enabled by its modular design. It's based on a powertrain system with a dual motor driving scheme and a rechargeable Lithium-ion battery. The powertrain platform is be self-contained, with ports to mount different modules upon for flexible configurations. The first module being designed for it is a system of sensors to detect air quality and report it to a mobile app on a user’s device. Other modules may be designed, and need only implement a standard interface of communication to connect to the powertrain platform. The design is ongoing and will be subject to change as different components and technologies are weighed.


### Motivations
The motivations for designing and architecting this project stem from various factors. Firstly, my final embedded systems course, EECS 473, had a pesky requirement that all projects be “useful” and “marketable” rather than simply being fun to make. This project is more an exploration of the technologies in modern embedded systems, that incorporates all I learned in school as well as the analog hardware design I've learned during my tenure as an engineer -- in a fun package.

Secondly, it's my first solo project, building on my software and hardware knowledge while also serving as an exercise in design, manufacturing, and packaging with a bit of CAD and hands on crafting.


<img src="img/earlySketch.png" alt="drawing" width="600"/>


### Block Diagram
<img src="img/blockDiagram.png" alt="drawing" width="900"/>

### Major Themes

I wanted to make a robot (originally inspired by Star Wars Droids)

- I gave myself specific constraints:
    - I needed to use my own designed PCB as the central hub of system.
    - I needed to use DriverLib or HAL software, minimize things like Arduino.
    - I needed to be network of boards, with UART/I2C connections between them.
    - I (eventually) want to incorporate an RTOS.


### Project History and Progress So Far

#### Picking the chassis

I found some spare parts as mechanical basis
- Top - old MakeBlock kit Tank Chassis.
- Bottom - Tank Chassis from Amazon (for later variants).

<img src="img/chassis_1.jpeg" alt="drawing" width="400"/>

<img src="img/chassis_2.jpeg" alt="drawing" width="400"/>



#### Picking the brains

I knew I needed: 
- PWM output for 2-4 motors.
- I2C drivers for future modules.
- UART for connecting 2+ MCUs together.
- GPIO for LED output, debug, etc.

STM32 was a mature platform with good peripherals and driver library, so I designed the first iteration around a STM32F Dev board.

<img src="img/stm32.jpeg" alt="drawing" width="400"/>

#### Picking a communications platform

A Wi-Fi chip was also needed for my preferred communication (Wi-Fi sockets).
This was a fairly straightforward choice in hobbyist world - Espressif has best drivers and can use Arduino IDE, so I designed around an ESP8266 Dev board.

<img src="img/ESP8266.jpeg" alt="drawing" width="400"/>

#### Picking the batteries

The main determinants for picking a battery are capacity and voltage levels.
I had two Lithium-ion batteries from other products laying around:
- Top: A 3.7V rechargeable battery from Amazon RC car.
- Bottom: A 14.4V rechargeable battery from Shark Robot Vacuum. 

I wanted to leverage both for their strengths, as the 3.7V battery will be easily rechargeable and small, while the 14.4V battery will have a larger energy capacity between charges.

<img src="img/big_and_small.jpeg" alt="drawing" width="400"/>


#### Motor Drivers

The tank chassis both came with 12V brushed motors. This is pretty standard for brushed motors in small appliances, as motor power correlates with size of their coils.

<img src="img/chassis_1_motor.jpeg" alt="drawing" width="400"/>

I've worked with brushed motor drivers for a while, and had experience using the TI DRV8231 H-Bridge driver.

<img src="img/MotorDriver_subsystem.png" alt="drawing" width="400"/>


- This needed 3.3V reference voltage and 12V bus voltage.

#### How to power it all?

Now we had 2 MCU dev boards, 2 motors, and 2 potential battery voltages.
The big design challenge was this: How do I make power tree to work with all the different parts?

This took some iteration, but the below diagram shows my final architecture.
<img src="img/powerTree.png" alt="drawing" width="500"/>

I used a boost and a buck-boost to receive the battery voltage that could be ~3.6-15V.

The boost is to power motors (wanted high voltage, low current)

<img src="img/Boost_subsystem.png" alt="drawing" width="700"/>

While the buck-boost is to generate a 7.5V rail, and then then I used an LDO off of that to produce 3.3V for logic. 

Why not 5V? The reasoning here is that the ESP and STM32 boards have an onboard LDO to produce 5V, so I needed something higher than 5V before the LDO.

<img src="img/BuckBoost_subsystem.png" alt="drawing" width="700"/>


The Buck-Boost took several iterations to get right, and was generally the most difficult part of the project. Layout took a while to get right, so I made a separate board to work on the layout and test it without the other devices in the system.

<img src="img/buckboostPortion.jpeg" alt="drawing" width="700"/>

This took a few tries, but I learned a lot about power supply layout in the process. (I took an entire power electronics OCW course online)

<img src="img/buckboostPortion2.jpeg" alt="drawing" width="700"/>


The first major prototype board came together fairly well after debugging quite a few iterations. I did the schematic and layout in KiCAD, taking several years to study numerous tutorials on PCB crafting

<img src="img/layout_moduleo.png" alt="drawing" width="700"/>

<img src="img/prettySetup.jpeg" alt="drawing" width="700"/>

It was able to take in a battery input and power all the ICs successfully. 


<img src="img/fullsetup.jpeg" alt="drawing" width="700"/>

Another important piece was getting the controller. I started by making it connect to an iPhone/iPad app so I could start on a GUI that also reads sensor data. I coded up an entire app to have the useer input button presses to control speed and direction to the board.

<img src="img/phoneUI.PNG" alt="drawing" width="600"/>












