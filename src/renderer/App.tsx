// import { MemoryRouter as Router, Routes, Route } from 'react-router-dom';
import { HashRouter as Router, Routes, Route } from 'react-router-dom';
// import { HashRouter, Switch, Route } from 'react-router-dom'
import React from 'react';
import icon from '../../assets/icon.svg';
import './App.css';
import Launcher from './views/Launcher';
import AirClip from './views/AirClip';

const Hello = () => {
  return (
    <div>
      <div className="Hello">
        <img width="200" alt="icon" src={icon} />
      </div>
      <h1>electron-react-boilerplate</h1>
      <div className="Hello">
        <a
          href="https://electron-react-boilerplate.js.org/"
          target="_blank"
          rel="noreferrer"
        >
          <button type="button">
            <span role="img" aria-label="books">
              📚
            </span>
            Read our docs
          </button>
        </a>
        <a
          href="https://github.com/sponsors/electron-react-boilerplate"
          target="_blank"
          rel="noreferrer"
        >
          <button type="button">
            <span role="img" aria-label="books">
              🙏
            </span>
            Donate
          </button>
        </a>
      </div>
    </div>
  );
};

class Page extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  render() {
    return (
      <Router>
        <Routes>
          <Route element={<Launcher />} path="/" />
          <Route element={<AirClip />} path="/app/airclip" />
        </Routes>
      </Router>
    );
  }
}

export default Page;

// export default function App() {
//   return (
//     <Router>
//       <Routes>
//         <Route path="/" element={<Hello />} />
//       </Routes>
//     </Router>
//   );
// }
