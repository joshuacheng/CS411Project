import React from 'react';
import { Route, BrowserRouter as Router, Link } from "react-router-dom";
import Button from "@material-ui/core/Button";
import { withStyles } from "@material-ui/styles";
import SubmitForm from "./SubmitForm";
import AddInfo from "./submit/AddInfo";
import './App.css';
import UpdateCollege from './updateCollege/updateCollege';
import InsertCollege from './insertCollege/insertCollege';
import Regions from './regionColleges/regions';

const links = [
	{
		name: "Home",
		link: "/"
	},
	{
		name: "Insert / Delete applicant",
		link: "/submit"
	},
	{
		name: "Update college",
		link: "/updateCollege"
	},
	{
		name: "Insert college",
		link: "/insertCollege"
	},
	{
		name: "Find regionally competitive colleges",
		link: "/region"
	}
]

function App() {
  return (
    <div className="App">
		<Router>
      <header className="App-header">
        <h1>
          AdmitMe
        </h1>
		<div styles={{
			display: "flex",
			justifyContent: "flex-end"
		}}>
			{
				links.map((link, idx) => {
					return (
						<Button key={idx} component={Link} to={link.link}>
							{link.name}
						</Button>
					)
				})
			}
		</div>
      </header>

		
			<Route exact path="/" component={SubmitForm}/>
			<Route exact path="/region" component={Regions}/>
			<Route exact path="/submit" component={AddInfo}/>
			<Route exact path="/updateCollege" component={UpdateCollege}/>
			<Route exact path="/insertCollege" component={InsertCollege}/>
		</Router>
        {/* <SubmitForm /> */}
    </div>
  );
}

export default App;
