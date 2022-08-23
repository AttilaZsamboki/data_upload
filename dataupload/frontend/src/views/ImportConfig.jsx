import React, { useEffect } from "react";
import DataFrame from "../components/DataFrame";
import Userfront from "@userfront/react";
import { Navigate } from "react-router-dom";

export default function SpecialQueries() {
	if (!Userfront.accessToken()) {
		return <Navigate to='/login' />;
	}

	const tablePrefix = Userfront.user.name.slice(0, 3) + "_";
	const tables = ["templates", "special-queries"];

	useEffect(() => {
		document.title = "Import Config";
	}, []);

	return (
		<div>
			<DataFrame
				tables={tables}
				initialFilter={(input) => input.table.slice(0, 4).toLowerCase() === tablePrefix.toLowerCase()}
				dataPickerLabel='Config neve'
				prefix={false}
			/>
		</div>
	);
}
