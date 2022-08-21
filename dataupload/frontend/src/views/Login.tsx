import Userfront from "@userfront/react";
import React from "react";
import { Navigate } from "react-router-dom";

Userfront.init("6nz455rn");

const LoginForm = Userfront.build({
	toolId: "kabrlk",
});

class Login extends React.Component {
	render() {
		return <LoginForm />;
	}
}

export default Login;
