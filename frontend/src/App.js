import React, { useState, useEffect, useRef } from "react";
import io from 'socket.io-client';
import './App.css';
import Reactplayer from 'react-player'

const socket = io('http://localhost:8000');

function App() {

 //Input values
 const [temp, setTemp] = useState(1);
 const [ultrasonic, setUltrasonic] = useState(null);
 const [humidity, setHumidity] = useState(null);
 const [speed, setSpeed] = useState(1);

 useEffect(() => {
   // Listen for temperature updates
   socket.on('temp', (data) => {
     setTemp(data);
   });

   // Listen for ultrasonic updates
   socket.on('ultrasonic', (data) => {
     setUltrasonic(data);
   });
   // Listen for humidity updates
   socket.on('humidity', (data) => {
     setHumidity(data);
   });

   return () => {
     socket.off('temp');
     socket.off('ultrasonic');
     socket.off('humidity')
   };
 }, []);

 // This will handle the key presses within the webpage.
 useEffect(() => {
  // When a key is pressed down, depending on the key press, a certain outcome will be processed.
   const handleKeyDown = (event) => {
     if (event.key === 'w')
     {
       sendDirection("forward");
       sendSpeedVAlue(speed);
     }
     else if (event.key === 'a')
     {
       sendDirection("left");
       sendSpeedVAlue(speed);
     }
     else if (event.key === 's')
     {
       sendDirection("backward");
       sendSpeedVAlue(speed);
     }
     else if (event.key === 'd')
     {
       sendDirection("right");
       sendSpeedVAlue(speed);
     }
     else if (event.key === 't')
     {
       sendArmValue("forward");
     }
     else if (event.key === 'g')
     {
       sendArmValue("backward")
     }
     else if (event.key === 'f')
     {
       sendArmValue("right-rotate");
     }
     else if (event.key === 'h')
     {
       sendArmValue("left-rotate")
     }
     else if (event.key === 'i')
     {
       sendArmValue("arm-up");
     }
     else if (event.key === "k")
     {
       sendArmValue("arm-down");
     }
     else if (event.key === 'j')
     {
       sendPinchValue("grab");
     }
     else if (event.key === 'l')
     {
       sendPinchValue("release");
     }
     else if (event.key === 'n')
     {
       sendLightValue("on")
     }
     else if (event.key === 'm')
     {
       sendLightValue("off")
     }
   }
   // This handles what happens when a key is lifted/let go.
   const handleKeyUp = () => {
     sendDirection("stop")
     sendPinchValue("stop")
   }

   window.addEventListener('keydown', handleKeyDown)
   window.addEventListener('keyup', handleKeyUp)

   return () => {
     window.removeEventListener('keydown', handleKeyDown)
     window.addEventListener('keyup', handleKeyUp)
   }
 });

//  Functions for sending messages to MQTT broker through socket
 const sendDirection = (direction) => {
   socket.emit('send-direction', direction);
 };

 const sendArmValue = (value) => {
   socket.emit('send-arm-value', value);
 };

 const sendPinchValue = (value) => {
   socket.emit('send-pinch-value', value)
 }

 const sendLightValue = (value) => {
   socket.emit('send-light-value', value)
 }

 const sendSpeedVAlue = (value) => {
   socket.emit('send-speed-value', value)
 }


  
  return (
    <div className="App">
      <div className="App">
        {/* This will be the header. */}
      <div className="header-container">
        <div className="header-left">
          <img className='hack-logo' src='Hack 24 Logo.png' alt='hack logo'></img>
        </div>
        <div className="header-mid">
        <img className='team-logo' src='The Technicians Logo.png' alt='team logo'></img>
        </div>
        <div className="header-right">
          <h1>The Technicians</h1>
        </div>
      </div>
      {/* This will be the container for the "Our Mission" section of the webpage. */}
      <div className="mission-container">
        <h1>Our Mission</h1>
        <p>We have been tasked the grave task of reacreating the Mars rover in just 3 days.</p> 
        <p>The rover must be equipped to explore every facet of the Martain landscape, unlocking secrets of the world never before touched by human ingenuity.</p>
        <p>Although the mission will be daunting and full of hardships, we, the technicians must prevail to help humanity reach new frontiers.</p>
      </div>
      {/* This will be the containter for the "Our Team" section of the webpage where we will introduce all four members of the team. */}
      <div className="team-intro">
        <h1>Our Team</h1>
        <div className="member-grid">
          <img className="member-photo" src="Philemon_photo.jpg" alt='philemon'></img>
          <p>Hi, my name is Philemon. I'm transferring from Pasadena City College and I'm a Computer Engineering Major'.</p>
          <img className="member-photo" src="Min_photo.png" alt='min'></img>
          <p>Hi, my name is Min. I'm transferring from De Anza College and I'm an Electrical Engineering Major.</p>
          <img className="member-photo" src="diego_photo.jpg" alt="diego"></img>
          <p>Hi, my name is Diego. I'm transferring from East Los Angeles College and I'm an Aerospace Engineering Major.'</p>
          <img className="member-photo" src="Thaddeus_photo.jpg" alt="thaddeus"></img>
          <p>Hi, my name is Thaddeus. I'm transferring from Rio Hondo College and I'm an Electrical Engineering Major.</p>
        </div>
      </div>
      {/* This will be the container for the "Our Journey" section of the webpage. */}
      <div className="progress-container">
        <h1>Our Journey</h1>
        {/* The progress container will be split into 3 sections, one for each day. */}
        <div className="dayOfHAcK">
          <h2>First Day of HAcK 24</h2>
          <div className="progress-grid">
            <img className="progress-photo" src="Day1Intro.JPG" alt='day 1 intro'></img>
            <p>Beginning of HAcK 24, Wes explaining last details about HAcK.</p>
            <img className="progress-photo" src="JonAOverview.JPG" alt='jonathan'></img>
            <p>Dr. Jonathan Arenberg, a Northrop Grumman Fellow leding engineering and concept development for future sharing some insights and advice.</p>
            <img className="progress-photo" src="firstIterationOfWebsite.JPG" alt='first iteration website'></img>
            <p>This is the first iteration of the react website.</p>
            <img className="progress-photo" src="firstMotorTest.JPG" alt="first motor test"></img>
            <p>Our first time testing how the motors and the wheels function.</p>
            <img className="progress-photo" src="northropEngineer.jpg" alt="Katheryn"></img>
            <p>Our designated Northrop Grumman Engineer, Katheryn, reviewing our design pitch.</p>
            <img className="progress-photo" src="first3DPrint.JPG" alt="first 3D print"></img>
            <p>Our first 3D printed component before the end of Day 1.</p>
          </div> 
        </div>
        <div className="dayOfHAcK">
          <h2>Second Day of HAcK 24</h2>
          <div className="progress-grid">
            <img className="progress-photo" src="testingMotorControllers.JPG" alt="testing motor controller"></img>
            <p>We began testing how the motor controllers work and how are they suppose to be wired up.</p>
            <img className="progress-photo" src="implementingCamera.JPG" alt="implementing camera"></img>
            <p>We searched online to find out how the ESP32 microcontroller and the camera module worked. We were successful in setting up a browser video feed.</p>
            <img className="progress-photo" src="cameraDone.JPG" alt="camera done"></img>
            <p>We successfully embedded the browser camera feed into our react website.</p>
            <img className="progress-photo" src="firstLaserCut.JPG" alt="first laser cut"></img>
            <p>This is our first time using a laser cutting machine and the first laser cut component we made was the first iteration of the claws and a gear.</p>
            <img className="progress-photo" src="diegoLaserCutting.JPG" alt="diego laser cutting"></img>
            <p>Diego familiarizing himself with the laser cutting machine with the help of one of the HAcK mentors, Ryan.</p>
            <img className="progress-photo" src="testingServos.JPG" alt="testing servos"></img>
            <p>Here we are testing out the servos and decided to use the servos for the arm movement like moving forward and backward, angle the arm up or down. As a result, we decided to use 2 servos.</p>
            <img className="progress-photo" src="HAcKActivity.JPG" alt="hack activity"></img>
            <p>Before the dinner of Day 2 of HAcK, Wes and the mentors organized activities to allow the participants to get to know the other participants.</p>
            <img className="progress-photo" src="endOfDay2HAcK.JPG" alt="end of day 2"></img>
            <p>End of Day 2 of HAcK, we are able to wire the motor controllers and the servos to the Raspberry Pi Pico and have code that successfully utilizes them.</p>
          </div>
        </div>
        <div className="dayOfHAcK">
          <h2>Final day of HAcK</h2>
          <div className="progress-grid">
            <img className="progress-photo" src="troubleshootingSensors.JPG" alt="troubleshooting sensors"></img>
            <p>Here we encountered issues with running the ultrasonic sensor and the temperature and humidity sensor. With the help of Marvin, one of our HAcK mentors, we were able to fix the issue.</p>
            <img className="progress-photo" src="armStuck.JPG" alt="arm stuck"></img>
            <p>Right before lunch, we accidentally applied super glue onto the table and then placed our newly assembled arm onto the table, thus, causing it to be stuck to the table. Thankfully, with the help of two HAcK mentors, Ashley and Aniket, we are able to resolve the situation.</p>
            <img className="progress-photo" src="rewiringCircuits.JPG" alt="rewiring circuits"></img>
            <p>After further testing to ensure all parts worked, we began to rewire everything so that it would look more organized. This was later undone due to unforseen circumstances.</p>
            <img className="progress-photo" src="assemblingRover.jpg" alt="assembling rover"></img>
            <p>After rewiring, we started to assemble our rover as seen in this photo.</p>
            <img className="progress-photo" src="troubleshootingRover.jpg" alt="troubleshooting rover"></img>
            <p>Towards the end of the HAcK, we discovered that our pico might be fried as Thaddeus managed to burn his thumb on the pico. Because of this we had to change to a new pico which caused some problems with the MQTT. The inputs in the website no longer effects the rover.</p>
            <img className="progress-photo" src="finalSetupRover.jpg" alt="final setup rover"></img>
            <p>Before our final field test, we had 9 minutes of setup and during then we found out that the second pico seems to be malfunctioning so we had to change to our third pico with the help of Sina and Jaelyn, two of our HAcK mentors. During the final field test, we were able to have the camera and the ultrasonic sensor to work but nothing else was working. We also had issues with the pico not connecting to my laptop directly which we have no idea of what the cause was.</p>
          </div>
        </div>
      </div>
      {/* The end of the website would be the control center for the rover. */}
      <div className="control-center-header">
        <h1>Control Center</h1>
      </div>
      <div className="control-center-container">
        {/* Keybinds for the rover will be displayed on the left of the control center. */}
        <div className="control-center-left">
          <h2>Keybinds</h2>
          <div className="keybind-grid">
            <h4>w</h4>
            <h4>Forward</h4>
            <h4>a</h4>
            <h4>Rotate Left</h4>
            <h4>s</h4>
            <h4>Backward</h4>
            <h4>d</h4>
            <h4>Rotate Right</h4>
            <h4>t</h4>
            <h4>Arm Reach Forward</h4>
            <h4>g</h4>
            <h4>Arm Reach Backward</h4>
            <h4>f</h4>
            <h4>Arm Rotate Left</h4>
            <h4>h</h4>
            <h4>Arm Rotate Right</h4>
            <h4>i</h4>
            <h4>Arm Angle Up</h4>
            <h4>j</h4>
            <h4>Grab</h4>
            <h4>k</h4>
            <h4>Arm Angle Down</h4>
            <h4>l</h4>
            <h4>Release</h4>
            <h4>n</h4>
            <h4>Turn On LED</h4>
            <h4>m</h4>
            <h4>Turn Off LED</h4>
          </div>
        </div>
        {/* This is for displaying the camera feed in the website. */}
        <div className="control-center-mid">
          <h2>Camera POV</h2>
          <iframe width="800" height="600" src="http://192.168.50.53"></iframe>
        </div>
        {/* Statistics like temperature, humidity, distance will be displayed on the right of the control center. */}
        <div className="control-center-right">
          <h2>Statistics</h2>
          <p>Temperature in C is: {temp}</p>
          <p>Humidity is: {humidity}</p>
          {ultrasonic > 250 ? (
            <p>
              The field is clear
            </p>
          ) : (
            <p>
              An obstacle is {ultrasonic} cm away
            </p>
          )}
        </div>
      </div>
      {/* This is the motor speed slider for the wheel motors. */}
        <div>
          <input 
            type="range"
            min={50000}
            max={65535}
            step={100}
            value={speed}
            onChange={(e) => {
              setSpeed(e.target.valueAsNumber)
            }}
          />
        </div>
        <div>
          <p>final speed: {speed}</p>
        </div>
    </div>
    </div>
  );
}

export default App;