import React, { useEffect, useState, useRef } from "react";
import axios from "axios";
import { Autocomplete, Button, TextField } from "@mui/material";
import getCookie from "../utils/GetCookie";

// ag-grid
import { AgGridReact } from "ag-grid-react";

// css
import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-alpine.css";
import { useMemo } from "react";

export default function DataFrame({ tables, initialFilter }) {
	// static const variables

	const gridRef = useRef();
	const csrftoken = getCookie("csrftoken");

	const [tableName, setTablename] = useState();
	const handleChange = (event, values) => {
		setTablename(values);
	};

	const [rowData, setRowData] = useState([]);
	const [columnDefs, setColumnDefs] = useState([]);
	// fetching data from the database
	useEffect(() => {
		axios(`/api/${tableName}`).then((result) => setRowData(result.data.filter(initialFilter)));

		setColumnDefs([]);
	}, [tableName]);

	useEffect(() => {
		for (let data in rowData[0]) {
			if (data === Object.keys(rowData[0])[0]) {
				setColumnDefs((prev) => [...prev, { field: data, checkboxSelection: true }]);
			} else {
				setColumnDefs((prev) => [...prev, { field: data }]);
			}
		}
	}, [rowData]);

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

	return (
		<div>
			<Autocomplete
				disablePortal
				id='combo-box-demo'
				options={tables}
				sx={{ width: 300 }}
				renderInput={(params) => <TextField {...params} label='Table name' />}
				onChange={handleChange}
			/>
			<Button
				variant='contained'
				disabled={!tableName}
				sx={{
					"backgroundColor": "#057D55",
					"marginTop": 5,
					"marginLeft": 3,
					"&:hover": { color: "white" },
				}}
				href={`/add-${tableName}`}>
				Add row to {tableName}
			</Button>
			<div className='ag-theme-alpine' style={{ width: "100%", height: 700, marginTop: 50 }}>
				<AgGridReact
					ref={gridRef}
					defaultColDef={defaultColDef}
					rowSelection={"multiple"}
					enableRangeSelection={"true"}
					rowData={rowData}
					columnDefs={columnDefs}
				/>
			</div>
		</div>
	);
}
