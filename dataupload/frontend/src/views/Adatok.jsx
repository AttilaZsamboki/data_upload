import React, { useEffect } from "react";
import DataFrame from "../components/DataFrame";
import Userfront from "@userfront/react";
import { Navigate } from "react-router-dom";
import { useState } from "react";

export default function Tables() {
	if (!Userfront.accessToken()) {
		return <Navigate to='/login' />;
	}
	const tablePrefix = Userfront.user.name.slice(0, 3) + "_";
	const [tables, setTables] = useState([]);

	useEffect(() => {
		fetch("/api/table-names")
			.then((response) => response.json())
			.then((json) =>
				setTables(
					json.filter(
						(table) =>
							table.slice(0, 4).toLowerCase() ===
							tablePrefix.toLowerCase()
					)
				)
			);
	}, []);

	return <DataFrame tables={tables} filter={(input) => input} />;
}
