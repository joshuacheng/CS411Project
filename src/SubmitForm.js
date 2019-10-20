import React, { Component } from 'react'
import TextField from "@material-ui/core/TextField";
import Button from "@material-ui/core/Button";
import { withStyles } from "@material-ui/styles";

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
    }
});

const fields = [
    ['gpa', 0, 'GPA'],
    ['actScore', 0, 'ACT Score'],
    ['satScore', 0, 'SAT Score'],
    ['tuitionLower', 0, 'Minimum tuition'],
    ['tuitionUpper', 0, 'Maximum tuition']
]

export class SubmitForm extends Component {

    state = fields.reduce((state, field) => {
        return {...state, [field[0]]: field[1]}
    }, {})

    handleChange = name => event => {
        this.setState({
            [name]: event.target.value
        })
    }

    submit = event => {

    }

    render() {
        const { classes } = this.props;

        return (
            <div>
                <div className={classes.container}>
                {
                    fields.map(field => {
                        return (
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
                                placeholder={field[1]}
                                className={classes.textField}
                                label={field[2]}
                                value={this.state[field[0]]}
                                onChange={this.handleChange(field[0])}
                                margin="normal"
                            />
                        )
                    })
                    }
                    <Button
                        style={{alignSelf: "center"}}
                        variant="contained"
                        color="primary"
                        onSubmit={this.submit}
                        fullWidth={false}
                    >
                        Check your colleges!
                </Button>
                </div>
                
            </div>
        )
    }
}

export default withStyles(styles)(SubmitForm);
