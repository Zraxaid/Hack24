import logo from './logo.svg';
import './App.css';

function App() {
  return (
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
        </div>
        <div className="control-center-mid">
          <h2>Camera POV</h2>
        </div>
        <div className="control-center-right">
          <h2>Statistics</h2>
        </div>
      </div>
    </div>
  );
}

export default App;
