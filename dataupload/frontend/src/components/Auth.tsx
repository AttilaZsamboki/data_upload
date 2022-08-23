import React from "react";
import Userfront from "@userfront/react";
import { Button } from "@mui/material";

Userfront.init("6nz455rn");

export default class LogoutButton extends React.Component {
	constructor(props) {
		super(props);

		this.handleCLick = this.handleCLick.bind(this);
	}

	handleCLick(event) {
		event.preventDefault();
		Userfront.logout();
	}

	render() {
		return (
			<button id='logout-button' onClick={this.handleCLick}>
				Kijelentkezés
			</button>
		);
	}
}
