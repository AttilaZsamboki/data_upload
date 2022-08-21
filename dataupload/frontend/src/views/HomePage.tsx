import React from "react";
import userfront from "@userfront/react";
import { Navigate } from "react-router-dom";

export default function HomePage() {
	if (!Userfront.accessToken()) return <Navigate to='/login' />;
	return <h1>Home</h1>;
}
