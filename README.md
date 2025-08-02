# Moduleo

### Introduction
In short, Moduleo is a robot. One that can do a handful of tasks, enabled by its modular design. It's based on a powertrain system with a dual motor driving scheme and a rechargeable Lithium-ion battery. The powertrain platform is be self-contained, with ports to mount different modules upon for flexible configurations. The first module being designed for it is a system of sensors to detect air quality and report it to a mobile app on a user’s device. Other modules may be designed, and need only implement a standard interface of communication to connect to the powertrain platform. The design is ongoing and will be subject to change as different components and technologies are weighed.


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

I used a boost and a buck-boost to receive VIN that could be ~3.6-15V .

- I used the boost to power motors (wanted high voltage, low current).
<img src="img/Boost_subsystem.png" alt="drawing" width="400"/>
- I used the buck-boost to generate 7.5V rail, and then an LDO off of that to produce 3.3V for logic.
<img src="img/BuckBoost_subsystem.png" alt="drawing" width="400"/>
<img src="img/buckboostPortion.jpeg" alt="drawing" width="300"/>


<img src="img/fullsetup.jpeg" alt="drawing" width="300"/>


<img src="img/phoneUI.PNG" alt="drawing" width="300"/>


<img src="img/prettySetup.jpeg" alt="drawing" width="300"/>


<img src="img/layout_moduleo.png" alt="drawing" width="300"/>






