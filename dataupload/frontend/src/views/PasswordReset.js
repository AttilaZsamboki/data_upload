import { jsx as _jsx } from "react/jsx-runtime";
import React from 'react';
import Userfront from "@userfront/react";
import { Navigate } from "react-router-dom";
Userfront.init("6nz455rn");
const PasswordResetForm = Userfront.build({
    toolId: "amndlo"
});
export default class PwdReset extends React.Component {
    render() {
        if (Userfront.accessToken()) {
            return (_jsx(Navigate, { to: "/" }));
        }
        return _jsx(PasswordResetForm, {});
    }
}
