import React, { useEffect, useState, useRef } from "react";
import axios from "axios";
import { Autocomplete, Button, TextField } from "@mui/material";
import getCookie from "../utils/GetCookie";

// ag-grid
import { AgGridReact } from "ag-grid-react";

// css
import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-alpine.css";

export default function DataFrame({ tables, filter }) {
	// static const variables

	const gridRef = useRef();

	const csrftoken = getCookie("csrftoken");

	const [gridApi, setGridApi] = useState(null);
	const [gridColumnApi, setGridColumnApi] = useState(null);

	const [deleteRowId, setDeleteRowId] = useState([]);

	const onGridReady = (params) => {
		setGridApi(params.api);
		setGridColumnApi(params.columnApi);
	};

	const onSuppressKeyboardEvent = (params) => {
		if (!params.editing) {
			let isBackspaceKey = params.event.keyCode === 8;
			let isDeleteKey = params.event.keyCode === 46;

			// Delete selected rows with back space

			if (isBackspaceKey || isDeleteKey) {
				const selectedRows = params.api.getSelectedRows();

				setRowData(
					rowData.filter((row) => {
						return selectedRows.indexOf(row) == -1; // filter out selected rows
					})
				);

				setDeleteRowId(selectedRows);

				return true;
			}

			return false;
		}
	};

	const [tableName, setTablename] = useState();
	const handleChange = (event, values) => {
		setTablename(values);
	};

	const [rowData, setRowData] = useState([]);
	const [columnDefs, setColumnDefs] = useState([]);
	// fetching data from the database
	useEffect(() => {
		axios(`/api/${tableName}`).then((result) =>
			setRowData(result.data.filter(filter))
		);

		setColumnDefs([]);
	}, [tableName]);

	useEffect(() => {
		for (let data in rowData[0]) {
			if (data === Object.keys(rowData[0])[0]) {
				setColumnDefs((prev) => [
					...prev,
					{ field: data, checkboxSelection: true },
				]);
			} else {
				setColumnDefs((prev) => [...prev, { field: data }]);
			}
		}
	}, [rowData]);

	// posting data to the database
	useEffect(() => {
		const rowId = deleteRowId.map((rowId) => rowId.id);
		fetch(`/api/${tableName}/${rowId}`, {
			method: "DELETE",
			headers: {
				Accept: "application/json",
				"X-CSRFToken": csrftoken,
				"Content-Type": "application/json",
			},
		});
	}, [deleteRowId]);

	return (
		<div>
			<Autocomplete
				disablePortal
				id='combo-box-demo'
				options={tables}
				sx={{ width: 300 }}
				renderInput={(params) => (
					<TextField {...params} label='Table name' />
				)}
				onChange={handleChange}
			/>
			<Button
				variant='contained'
				disabled={!tableName}
				sx={{
					backgroundColor: "#057D55",
					marginTop: 5,
					marginLeft: 3,
					"&:hover": { color: "white" },
				}}
				href={`/add-${tableName}`}>
				Add row to {tableName}
			</Button>
			<div
				className='ag-theme-alpine'
				style={{ width: 1335, height: 500, marginTop: 50 }}>
				<AgGridReact
					ref={gridRef}
					getRowId={(n) => n.id}
					rowSelection={"multiple"}
					enableRangeSelection={"true"}
					onGridReady={onGridReady}
					rowData={rowData}
					defaultColDef={{
						suppressKeyboardEvent: onSuppressKeyboardEvent,
					}}
					columnDefs={columnDefs}
				/>
			</div>
		</div>
	);
}
