import React, { useState } from "react";
import DataFrame from "../components/DataFrame";
import Autocomplete from "@mui/material/Autocomplete";
import { TextField } from "@mui/material";
import Userfront from "@userfront/react";
import { Navigate } from "react-router-dom";

export default function SpecialQueries() {
	if (!Userfront.accessToken()) {
		return <Navigate to='/login' />;
	}

	const tables = ["templates", "special-queries"];

	const filter = (input) => input.created_by_id === Userfront.user.userId;

	return (
		<div>
			<DataFrame tables={tables} initialFilter={filter} dataPickerLabel='Config neve' prefix={false} />
		</div>
	);
}
