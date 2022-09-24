import React from "react";
import Userfront from "@userfront/react";
import { Navigate } from "react-router-dom";

Userfront.init("6nz455rn");

const SignupForm = Userfront.build({
	toolId: "mmorlo",
});

export default class Signup extends React.Component {
	componentDidMount() {
		document.title = "Regisztrálás";
	}

	render() {
		if (!Userfront.accessToken()) {
			return <Navigate to='/' />;
		} else if (Userfront.user.data && !Userfront.user.data.access === "admin") {
			return <Navigate to='/upload' />;
		}
		return <SignupForm />;
	}
}
