import React from "react";
import Userfront from "@userfront/react";
import { Navigate } from "react-router-dom";

Userfront.init("6nz455rn");

const PasswordResetForm = Userfront.build({
	toolId: "amndlo",
});

export default class PwdReset extends React.Component {
	render() {
		if (!Userfront.accessToken()) {
			return <Navigate to='/login' />;
		}
		return <PasswordResetForm />;
	}
}
