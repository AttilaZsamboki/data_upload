import * as React from "react";
import { useTable, useTableOptions } from "../hooks/Tables";
import { Autocomplete, TextField, Button } from "@mui/material";
import Userfront from "@userfront/react";
import { Navigate } from "react-router-dom";

import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-alpine.css";
import { useState } from "react";
import { AgGridReact } from "ag-grid-react";
import { useEffect, useMemo } from "react";

function DataFrame({ importConfig }: { importConfig: boolean }) {
	const [inputTable, setInputTable] = useState<string | unknown>();
	const [columnDefs, setColumnDefs] = useState(null);
	const tables: any = importConfig ? { data: ["Templates", "Special queries"] } : useTableOptions();
	const table: any = useTable(inputTable);

	useEffect(() => {
		if (table.data) {
			setColumnDefs(Object.keys(table.data[0]).map((col) => ({ field: col })));
		}
	}, [table]);

	const defaultColDef = useMemo(
		() => ({
			floatingFilter: true,
			filter: true,
			minWidth: 200,
			flex: 1,
			filterParams: {
				debounceMs: 0,
			},
		}),
		[]
	);

	if (tables.isLoading) return <span>Loading...</span>;
	if (tables.isError) return <span>Error: {tables.error.message}</span>;
	return (
		<>
			<Autocomplete
				id='table'
				options={tables.data}
				sx={{ width: 300 }}
				renderInput={(params) => <TextField {...params} label={"Table name"} />}
				onChange={(e, v) => setInputTable(v)}
			/>
			{importConfig && typeof inputTable === "string" && (
				<Button
					variant='contained'
					href={`/add-${inputTable.toLowerCase().replace(" ", "-")}/`}
					disabled={!inputTable}>{`Add-${inputTable ? inputTable : ""}`}</Button>
			)}
			<div className='ag-theme-alpine' style={{ width: "100%", height: 700, marginTop: 50 }}>
				<AgGridReact
					defaultColDef={defaultColDef}
					rowSelection={"multiple"}
					rowData={table.data}
					columnDefs={columnDefs}
				/>
			</div>
		</>
	);
}

export function Adatok() {
	if (!Userfront.accessToken()) {
		return <Navigate to='/login' />;
	}

	useEffect(() => {
		document.title = "Adatok";
	}, []);

	return <DataFrame importConfig={false} />;
}

export function ImportConfig() {
	if (!Userfront.accessToken()) {
		return <Navigate to='/login' />;
	}

	useEffect(() => {
		document.title = "ImportConfig";
	}, []);

	return <DataFrame importConfig={true} />;
}
