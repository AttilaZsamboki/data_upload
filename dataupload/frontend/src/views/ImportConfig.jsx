import React, { useEffect } from "react";
import DataFrame from "../components/DataFrame";
import Userfront from "@userfront/react";
import { Navigate } from "react-router-dom";

export default function SpecialQueries() {
	if (!Userfront.accessToken()) {
		return <Navigate to='/login' />;
	}

	const tables = ["templates", "special-queries"];

	const filter = (input) => input.created_by_id === Userfront.user.userId;

	useEffect(() => {
		document.title = "Import Config";
	}, []);

	return (
		<div>
			<DataFrame tables={tables} initialFilter={filter} dataPickerLabel='Config neve' prefix={false} />
		</div>
	);
}
