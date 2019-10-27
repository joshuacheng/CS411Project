import React, { Component } from 'react'
import TextField from "@material-ui/core/TextField";
import Button from "@material-ui/core/Button";
import Select from "@material-ui/core/Select";
import MenuItem from "@material-ui/core/MenuItem";
import InputLabel from "@material-ui/core/InputLabel";
import { withStyles } from "@material-ui/styles";
import * as d from "d3-fetch";

const styles = theme => ({
	button: {
		width: "50%"
	},
	supercontainer: {
		display: "flex",
		flexDirection: "row",
		justifyContent: "space-around"
	},
	container: {
		display: 'flex',
		flexDirection: 'column',
		width: "40%",
		marginLeft: "20px",
		marginTop: "100px",
		backgroundColor: "lightgray",
		padding: "40px"
	},
	deleteForm: {
		width: "40%",
		display: 'flex',
		flexDirection: 'column',
		backgroundColor: "lightgray",
		padding: "40px"
	},
	textField: {
		margin: "40px 10px",
	},
	textFieldDelete: {
		margin: "20px 10px"
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

// console.log(colleges);


const fields = [
	['testScore', 0, 'Test Score'],
	['gpa', 0, 'Unweighted GPA'],
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

export class AddInfo extends Component {

	state = fields.reduce((state, field) => {
		return { ...state, [field[0]]: field[1] }
	}, {
		category: '',
		testType: '',
		inOrOutOfState: '',
		deleteId: '',
		college: '',
		collegesGot: false
	})

	componentDidMount = async () => {
		this.colleges = await d.csv("/colleges.csv").then(data => {
			// console.log(Object.values(data).slice(0, -1));
			return Array.from(Object.values(data).slice(0, -1));
		});
		this.setState({ collegesGot: true });
	}

	handleChange = name => event => {
		this.setState({
			[name]: event.target.value
		})
	}

	submit = event => {

	}

	submitDelete = event => {

	}

	render() {
		const { classes } = this.props;

		return (
			<div>
				<p>
					Here you can submit info to our database!
					Note: SAT scores should be the new format (out of 1600)
				</p>
				<div className={classes.supercontainer}>
					<div className={classes.container}>
						<InputLabel htmlFor="test-type">Test Type</InputLabel>
						<Select
							className={classes.dropdown}
							inputProps={{
								name: 'Test Type',
								id: 'test-type'
							}}
							value={this.state.testType}
							onChange={this.handleChange('testType')}
						>
							<MenuItem value={"ACT"}>
								{"ACT"}
							</MenuItem>
							<MenuItem value={"SAT"}>
								{"SAT"}
							</MenuItem>
						</Select>
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
						<InputLabel htmlFor="in-out-state">In or out of state</InputLabel>
						< Select
							className={classes.dropdown}
							inputProps={{
								name: 'in or out of state',
								id: 'in-out-state'
							}}
							value={this.state.inOrOutOfState}
							onChange={this.handleChange('inOrOutOfState')}
						>
							<MenuItem value={"instate"}>
								{"In State"}
							</MenuItem>
							<MenuItem value={"outstate"}>
								{"Out of State"}
							</MenuItem>
						</Select>
						{this.state.collegesGot &&
							<div>
								<InputLabel htmlFor="accepted-college">College Accepted To</InputLabel>
								< Select
									className={classes.dropdown}
									inputProps={{
										name: 'college',
										id: 'accepted-college'
									}}
									value={this.state.college}
									onChange={this.handleChange('college')}
								>
									{
										this.colleges.map((c, idx) => {
											return (
												<MenuItem key={idx} value={c.Name}>
													{c.Name}
												</MenuItem>
											)
										})
									}
								</Select>
							</div>
						}
						<Button
							style={{ alignSelf: "center", marginTop: "100px" }}
							variant="contained"
							color="primary"
							onSubmit={this.submit}
							fullWidth={false}
						>
							Submit Info
                </Button>
					</div>
					<div className={classes.deleteForm}>
						<TextField
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
							placeholder={"ID to delete"}
							className={classes.textFieldDelete}
							label={"Delete data"}
							value={this.state['deleteId']}
							onChange={this.handleChange('deleteId')}
							margin="normal"
						/>
						<Button
							style={{ alignSelf: "center", marginTop: "100px" }}
							variant="contained"
							color="primary"
							onSubmit={this.submitDelete}
							fullWidth={false}
						>
							Delete by ID
                		</Button>
					</div>
				</div>
			</div >
		)
	}
}

export default withStyles(styles)(AddInfo);