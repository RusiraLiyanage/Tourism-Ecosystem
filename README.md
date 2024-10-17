# Toursim Ecosystem

## University of Wollongong

## CSCI927 Service Oriented Software Engineering

## Group Members

### Rusira Liyanage - 8275129
### Vincent Paul - 8752783
### Lamia Rahman - 7885568
### Ammad Aslam - 7732739
### Le Shi - 7890321
### Akhil Ayilavajjula - 7608901

### This Toursim Ecosystem contains following functionalities,

#### 1. Service Implementations using microservices approach with Rest APIs for the following selected services.

1.	Event Scheduling - provided by Event Organizers
2. Ride Booking - provided by Local Transporation
3. Table Reservations - provided by Resturants and cafes

#### 2. Process Simulations for the following selected services to generate event logs for process mining.

1. Event Scheduling - provided by Event Organizers
2. Ride Booking - provided by Local Transportation
3. Table Reservations - provided by Resturants and Cafes

## Getting started

### This project has been programmed using python programming language with flusk server 
### 1. Install python 

1. follow the following guide and install python in your pc

    For Windows Users - https://docs.python.org/3/using/windows.html <br>
    For Mac Users - https://docs.python.org/3/using/mac.html

### 2. Install Flask

1. Open a Terminal
3. Afterwards, run the following command to install flask server into your machine globally,
    ```
    pip install Flask
    ```

### 2. To run a Microservice

1. Open a Terminal
2. Navigate to the path of a specific microservice (Ex - cd ServiceProviders\EventOrganiers\Services\EventScheduling\Microservices\EventManagement \Microservice)
3. Afterwards, run the following command to start a specific microservice,
    ```
    python eventManagement.py
    ```
### 3. To run a Process Simulation

1.  Open a Terminal
2. Navigate to the path of a specific Process SImulation (Ex - cd cd ServiceProviders\EventOrganiers\Services\EventScheduling\Process Mining)
3. Afterwards, run the following command to run a manually generated process execution,
    ```
    python eventSchedulingSimulation.py
    ```
4. The generated log files can opend and observed using MS Excel software.

#### In this project, all the demo data used by microservices are maintained in their designated folders. This approach implies the need to manage seperate databases to manage data belongs to each microservices, when this infrastructure is deployed for real world usage.
