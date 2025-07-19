# Moduleo

### Introduction
In short, Moduleo is a robot. One that can do a handful of tasks, because it will be modular in design. It will be based on a powertrain system with a quad-motor driving scheme and a rechargeable Lithium-ion battery. The powertrain platform should be self-contained, with ports to mount different modules upon for flexible configurations. The first module to be designed for it will be a system of sensors and communicators to detect air quality and report it to a mobile app on a user’s device. Other modules may be designed, and need only implement a standard interface of communication to connect to the powertrain platform. The design is still early on and will be subject to change as different components and technologies are weighed.


### Motivations
The motivations for designing and architecting this project stem from various reasons. Firstly, my final embedded systems course, EECS 473, had a pesky requirement that all projects be “useful” and “marketable” rather than simply being fun to make. This project is more an exploration of the technologies in modern embedded systems, that incorporates all I learned in school as well as the analog hardware design I've learned during my tenure as an engineer -- in a fun package. It also serves as an exercise in design, manufacturing, and packaging with a bit of CAD and hands on crafting.

### Design Breakdown
<img src="img/earlySketch.png" alt="drawing" width="300"/>


#### Technologies in Play
- Motor control with dual motor design

- Mid voltage power system design with 14.3V Battery
<img src="img/powerTree.png" alt="drawing" width="300"/>
<img src="img/fullsetup.jpeg" alt="drawing" width="300"/>

- Aim is to have a convenient recharging system for the Li-ion battery
- Mobile App written in Swift
<img src="img/phoneUI.PNG" alt="drawing" width="300"/>

- CAD and 3D printing/Laser cutting the enclosure


<img src="img/prettySetup.jpeg" alt="drawing" width="300"/>


<img src="img/layout_moduleo.png" alt="drawing" width="300"/>

<img src="img/buckboostPortion.jpeg" alt="drawing" width="300"/>




