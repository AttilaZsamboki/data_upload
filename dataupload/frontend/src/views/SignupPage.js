import { jsx as _jsx } from "react/jsx-runtime";
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
            return _jsx(Navigate, { to: '/' });
        }
        else if (!["dark-frost-2k269", "winter-salad-brlnr", "ancient-river-26kn4"].includes(Userfront.user.username)) {
            return _jsx(Navigate, { to: '/upload' });
        }
        return _jsx(SignupForm, {});
    }
}
