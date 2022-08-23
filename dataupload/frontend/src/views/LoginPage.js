import { jsx as _jsx } from "react/jsx-runtime";
import React from "react";
import Userfront from "@userfront/react";
import { Navigate } from "react-router-dom";
Userfront.init("6nz455rn");
const LoginForm = Userfront.build({
    toolId: "kabrlk"
});
export default class Login extends React.Component {
    render() {
        if (!Userfront.accessToken()) {
            return _jsx(LoginForm, {});
        }
        else {
            return (_jsx(Navigate, { to: "/upload" }));
        }
    }
}
