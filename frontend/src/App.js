import React, { useState, useEffect, useRef } from "react";
import io from 'socket.io-client';
import './App.css';
import Reactplayer from 'react-player'

const socket = io('http://localhost:8000');


function App() {

  //Output values
  


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

  useEffect(() => {
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

  //functions for sending messages to MQTT broker through socket
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
        <p>Our goal is to recreate the mars rover. This will be modified later.</p>
      </div>
      {/* This will be the containter for the "Our Team" section of the webpage where we will introduce all four members of the team. */}
      <div className="team-intro">
        <h1>Our Team</h1>
        <div className="member-grid">
         <img className="philemon-photo" src="Philemon_photo.jpg" alt='philemon photo'></img>
         <p>Hi, my name is Philemon Chan. I am transferring from Pasadena City College and I major in Computer Engineering.</p>
        </div>
      </div>
      {/* This will be the container for the "Our Journey" section of the webpage. */}
      <div className="progress-container">
        <h1>Our Journey</h1>
        <div className="progress-grid">
          <img className="day1intro-photo" src="Day1Intro.JPG" alt='day 1 intro'></img>
          <p>First Day of HAcK, Wes explaining last details about HAcK.</p>
        </div>
      </div>
      <div className="control-center-header">
        <h1>Control Center</h1>
      </div>
      <div className="control-center-container">
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
        <div className="control-center-mid">
          <h2>Camera POV</h2>
          <iframe width="800" height="600" src="http://192.168.50.53"></iframe>
        </div>
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