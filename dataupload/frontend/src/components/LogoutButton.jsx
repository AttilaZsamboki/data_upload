import React from 'react';
import Userfront from "@userfront/react";

Userfront.init("6nz455rn");

export default class LogoutButton extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            disabled: !Userfront.tokens.accessToken,
        };

        this.handleCLick = this.handleCLick.bind(this);
    }

    handleCLick(event) {
        event.preventDefault();
        Userfront.logout();
    }

    render() {
        return (<button id="logout-button" onClick={this.handleCLick} disabled={this.state.disabled}>
                Logout
            </button>);
    }
}

