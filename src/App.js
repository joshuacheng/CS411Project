import React from 'react';
import { Route, BrowserRouter as Router } from "react-router-dom";
import Button from "@material-ui/core/Button";
import SubmitForm from "./SubmitForm";
import AddInfo from "./submit/AddInfo";
import './App.css';
import UpdateCollege from './updateCollege/updateCollege';

const links = [
	{
		name: "Home",
		link: "/"
	},
	{
		name: "Insert applicant",
		link: "/submit"
	},
	{
		name: "Update college",
		link: "/updateCollege"
	}
]

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>
          AdmitMe
        </h1>
		{/* <div className=> */}

		{/* </div> */}
      </header>

		<Router>
			<Route exact path="/" component={SubmitForm}/>
			<Route exact path="/submit" component={AddInfo}/>
			<Route exact path="/updateCollege" component={UpdateCollege}/>
			{/* <Route exact path+ */}
		</Router>
        {/* <SubmitForm /> */}
    </div>
  );
}

export default App;
