import { jsx as _jsx } from "react/jsx-runtime";
import React from "react";
import Userfront from "@userfront/react";
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
        return (_jsx("button", Object.assign({ id: 'logout-button', onClick: this.handleCLick }, { children: "Kijelentkez\u00E9s" })));
    }
}
