import React, { useState, useEffect, useRef } from "react";
import io from 'socket.io-client';
import './App.css';
import ReactPlayer from 'react-player'


const socket = io('http://localhost:8000');


function App() {


  const [temp, setTemp] = useState(null);
  const [ultrasonic, setUltrasonic] = useState(null);
  const [humidity, setHumidity] = useState(null);

  useEffect(() => {
    // Listen for temperature updates
    socket.on('temp', (data) => {
      setTemp(data);
    });

    // Listen for ultrasonic updates
    socket.on('ultrasonic', (data) => {
      setUltrasonic(data);
    });

    socket.on('humidity', (data) => {
      setHumidity(data);
    });

    return () => {
      socket.off('temp');
      socket.off('ultrasonic');
      socket.off('humidity')
    };
  }, []);

  const sendDirection = (direction) => {
    socket.emit('send-direction', direction);
  };

  const sendArmValue = (value) => {
    socket.emit('send-arm-value', value);
  };

  

  return (
    <div className="App">
      <div className="App">
      {/* <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header> */}
      {/* This is the header of the webpage and it will be always present. */}
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
            <h4>Up</h4>
            <h4>Arm Reach Forward</h4>
            <h4>Down</h4>
            <h4>Arm Reach Backward</h4>
            <h4>Left</h4>
            <h4>Arm Rotate Left</h4>
            <h4>Right</h4>
            <h4>Arm Rotate Right</h4>
            <h4>i</h4>
            <h4>Arm Angle Up</h4>
            <h4>j</h4>
            <h4>Grab</h4>
            <h4>k</h4>
            <h4>Arm Angle Down</h4>
            <h4>l</h4>
            <h4>Release</h4>
          </div>
        </div>
        <div className="control-center-mid">
          <h2>Camera POV</h2>
          <iframe width="800" height="600" src="http://192.168.50.53"></iframe>
        </div>
        <div className="control-center-right">
          <h2>Statistics</h2>
        </div>
      </div>
    </div>
    </div>
  );
}

export default App;
