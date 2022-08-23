import React from "react";
import Userfront from "@userfront/react";
import { Navigate } from "react-router-dom";

export default function HomePage() {
	if (!Userfront.accessToken()) return <Navigate to='/login' />;
	return (
		<div className='flex justify-center items-center'>
			<h1 className='text-tetriarydark'>Home Page</h1>
		</div>
	);
}
