import React from 'react';
import Button from "@material-ui/core/Button";
import SubmitForm from "./SubmitForm";
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        {/* <img src={logo} className="App-logo" alt="logo" /> */}
        <h1>
          AdmitMe
        </h1>
        <Button>
          get stuff
        </Button>
      </header>

        <SubmitForm />
    </div>
  );
}

export default App;
