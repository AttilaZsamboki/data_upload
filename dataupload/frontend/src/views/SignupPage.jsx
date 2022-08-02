import React from "react";
import Userfront from "@userfront/react";
import {Navigate} from "react-router-dom";

Userfront.init("6nz455rn");

const SignupForm = Userfront.build({
  toolId: "mmorlo"
});

export default class Signup extends React.Component {
  render () {
    if (Userfront.accessToken()) {
      return <Navigate to="/"/>
    }
    return <SignupForm />
  }
}