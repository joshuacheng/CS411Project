import React, { Component } from 'react'
import TextField from "@material-ui/core/TextField";
import Button from "@material-ui/core/Button";
import Select from "@material-ui/core/Select";
import MenuItem from "@material-ui/core/MenuItem";
import InputLabel from "@material-ui/core/InputLabel";
import { withStyles } from "@material-ui/styles";
import axios from "axios";

const styles = theme => ({
	button: {
		width: "50%"
	},
	super: {
		marginTop: "30px",
		display: 'flex',
		flexDirection: 'row'
	},
	container: {
		display: 'flex',
		flexDirection: 'column',
		width: "50%",
		marginLeft: "20px"
	},
	textField: {
		margin: "40px 10px",
	},
	textFieldFontSize: {
		fontSize: "50px"
	},
	inputLabel: {
		fontSize: "30px"
	},
	dropdown: {
		margin: "40px 10px"
	},
	header: {
		fontSize: '40px',
		textDecoration: 'underline'
	},
	level: {
		display: 'flex',
		flexDirection: 'column'
	}
});

const categories = [
	"CS/CE/EE/Software/IT",
	"Other Engineering",
	"Biology/Premed",
	"Math/Statistics",
	"Other Sciences",
	"Business/Econ/Accounting/Marketing",
	"Liberal Arts/Journalism",
	"Social Work/Other"
]

const regions = [
	'Midwest',
	'Northeast',
	'West',
	'South',
	'No Preference'
]

// const mockData = {
// 	"Most competitive": "Berk",
// 	"Least competitive": "Merced"
// }

export class Regional extends Component {

	state = {
		category: '',
		region: '',
		received: false,
		loading: false,
		collegesList: {}
	}

	// componentDidMount() {
	// 	this.setState({
	// 		collegesList: mockData,
	// 		received: true
	// 	})
	// }

	handleChange = name => event => {
		this.setState({
			[name]: event.target.value
		})
	}

	submit = event => {

		const body = {
			majorCategory: this.state.category,
			region: this.state.region
		}

		const url = `/competitive`;

		console.log('checking competitive colleges in this region...');

		this.setState({
			loading: true
		})
		axios.request({
			method: 'GET',
			url,
			baseURL: 'http://localhost:5000',
			data: body,
			headers: {
				'Content-Type': 'application/json',
				'Access-Control-Allow-Origin': '*',
			}
		}).then(res => {
			console.log(res);
			this.setState({
				received: true,
				loading: false,
				collegesList: res.data
			})
		}).catch(err => {
			console.log(err.message);
		})
	}

	render() {
		const { classes } = this.props;

		

		return (
			<div className={classes.super}>
				<div className={classes.container}>
					<InputLabel htmlFor="major-category">Major Category</InputLabel>
					< Select
						className={classes.dropdown}
						inputProps={{
							name: 'Major Category',
							id: 'major-category'
						}}
						value={this.state.category}
						onChange={this.handleChange('category')}
					>
						{
							categories.map((c, idx) => {
								return (
									<MenuItem key={idx} value={c}>
										{c}
									</MenuItem>
								)
							})
						}
					</Select>
					<InputLabel htmlFor="region">Region</InputLabel>
					< Select
						className={classes.dropdown}
						inputProps={{
							name: 'Region',
							id: 'region'
						}}
						value={this.state.region}
						onChange={this.handleChange('region')}
					>
						{
							regions.map((c, idx) => {
								return (
									<MenuItem key={idx} value={c}>
										{c.charAt(0).toUpperCase() + c.slice(1)}
									</MenuItem>
								)
							})
						}
					</Select>
					<Button
						style={{ alignSelf: "center", marginTop: "100px" }}
						variant="contained"
						color="primary"
						onClick={this.submit}
						fullWidth={false}
					>
						Check your colleges!
                	</Button>
					{
						this.state.loading &&
						<p>
							Results loading...
					</p>
					}
				</div>
				{
					this.state.received &&
					<div className={classes.container}>
						<div className={classes.level}>
							<h2 className={classes.header}>Most competitive college</h2>
							<p>{this.state.collegesList["Most Competitive"]}</p>
						</div>
						<div className={classes.level}>
							<h2 className={classes.header}>Least competitive college</h2>
							<p>{this.state.collegesList["Least Competitive"]}</p>
						</div>
					</div>
				}
			</div >
		)
	}
}

export default withStyles(styles)(Regional);
