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
	}
});

const fields = [
	['gpa', 0, 'GPA'],
	['actScore', 0, 'ACT Score'],
	['satScore', 0, 'SAT Score'],
	['tuitionLower', 0, 'Minimum tuition'],
	['tuitionUpper', 0, 'Maximum tuition'],
]

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
	'South'
]

export class SubmitForm extends Component {

	state = fields.reduce((state, field) => {
		return { ...state, [field[0]]: field[1] }
	}, {
		category: '',
		region: '',
		received: false,
		loading: false
	})

	handleChange = name => event => {
		this.setState({
			[name]: event.target.value
		})
	}

	submit = event => {
		const body = {
			GPA: this.state.gpa,
			actScore: this.state.actScore,
			satScore: this.state.satScore,
			maximumTuition: this.state.tuitionUpper,
			majorCategory: this.state.category,
			region: this.state.region
		}

		const url = `/matchColleges`;

		console.log('chancing...');

		this.setState({
			loading: true
		})
		axios.request({
			method: 'POST',
			url,
			baseURL: 'http://localhost:5000',
			data: body,
			headers: {
				'Content-Type': 'application/json',
				'Access-Control-Allow-Origin': '*',
			}
		}).then(res => {
			console.log(res.status);
			this.setState({
				received: true,
				loading: false
			})
		}).catch(err => {
			console.log(err.message);
		})
	}

	render() {
		const { classes } = this.props;

		return (
			<div>
				<div className={classes.container}>
					{
						fields.map((field, idx) => {
							return (
								<TextField
									key={idx}
									InputProps={{
										classes: {
											input: classes.textFieldFontSize
										}
									}}
									InputLabelProps={{
										classes: {
											shrink: false,
											root: classes.inputLabel
										},
									}}
									placeholder={String(field[1])}
									className={classes.textField}
									label={field[2]}
									value={this.state[field[0]]}
									onChange={this.handleChange(field[0])}
									margin="normal"
								/>
							)
						})}
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
				{
					this.state.received &&
					<p>
						Results will be displayed here soon tm
					</p>
				}
				</div>

			</div >
		)
	}
}

export default withStyles(styles)(SubmitForm);
