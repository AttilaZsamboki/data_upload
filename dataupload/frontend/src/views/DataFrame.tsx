import * as React from "react";
import { useTable, useTableOptions } from "../hooks/Tables";
import { Autocomplete, TextField, Button } from "@mui/material";
import Userfront from "@userfront/react";
import { Navigate } from "react-router-dom";
import getCookie from "../utils/GetCookie";
import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-material.css";
import { useState } from "react";
import { AgGridReact } from "ag-grid-react";
import { useEffect, useMemo } from "react";
import { Box } from "@mui/system";
import axios from "axios";

const csrftoken = getCookie("csrftoken");

function DataFrame({ importConfig }: { importConfig: boolean }) {
	const gridRef = React.useRef();
	const [inputTable, setInputTable] = useState<string>();
	const [columnDefs, setColumnDefs] = useState(null);
	const tables: any = useTableOptions();
	const table: any = useTable(inputTable);
	const importConfigTypes = ["Templates", "Special queries"];

	useEffect(() => {
		if (table.data && inputTable) {
			setColumnDefs(Object.keys(table.data[0]).map((col) => ({ field: col })));
		}
	}, [inputTable, table]);

	const defaultColDef = useMemo(
		() => ({
			floatingFilter: true,
			filter: true,
			minWidth: 200,
			editable: true,
			sortable: true,
			flex: 1,
			filterParams: {
				debounceMs: 0,
			},
		}),
		[]
	);

	const onBtWhich = (event: any) => {
		axios.put(`/api/${inputTable.toLowerCase().replace(" ", "-")}/${event.data.id}/`, event.data, {
			headers: {
				"X-CSRFToken": csrftoken,
				"Content-Type": "multipart/form-data",
			},
		});
	};

	const getRowId = useMemo(() => {
		return (params: any) => {
			return params.data.id;
		};
	}, []);

	return (
		<div>
			<h1 className='flex flex-col items-center justify-center mb-3'>
				{!importConfig ? "Adatok" : "Import Konfigurációk"}
			</h1>
			<Autocomplete
				className='m-auto flex flex-col items-center justify-center'
				id='table'
				options={importConfig ? importConfigTypes : tables.data}
				sx={{ width: 300 }}
				renderInput={(params) => <TextField {...params} label={importConfig ? "Konfig neve" : "Tábla neve"} />}
				onChange={(e, v) => setInputTable(v)}
			/>
			{importConfig && typeof inputTable === "string" && (
				<Box textAlign='center' marginTop={5}>
					<Button
						sx={{
							"&:hover": { color: "white" },
							"backgroundColor": "#057D55",
						}}
						variant='contained'
						href={`/add-${inputTable.toLowerCase().replace(" ", "-")}`}
						disabled={!inputTable}>{`${inputTable ? inputTable.slice(0, -1) : ""} hozzáadása`}</Button>
				</Box>
			)}
			<div className='mx-auto flex flex-col items-center justify-center '>
				<div className='ag-theme-material' style={{ width: "92%", height: 700, marginTop: 50 }}>
					<AgGridReact
						ref={gridRef}
						animateRows={importConfig ? true : false}
						defaultColDef={defaultColDef}
						rowSelection={"multiple"}
						rowData={table.data}
						columnDefs={columnDefs}
						getRowId={getRowId}
						stopEditingWhenCellsLoseFocus={true}
						onCellValueChanged={onBtWhich}
					/>
				</div>
			</div>
		</div>
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
