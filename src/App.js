import React from 'react';
import { Route, BrowserRouter as Router } from "react-router-dom";
import Button from "@material-ui/core/Button";
import SubmitForm from "./SubmitForm";
import AddInfo from "./submit/AddInfo";
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>
          AdmitMe
        </h1>
      </header>

		<Router>
			<Route exact path="/" component={SubmitForm}/>
			<Route exact path="/submit" component={AddInfo}/>
		</Router>
        {/* <SubmitForm /> */}
    </div>
  );
}

export default App;
