import React, { useEffect, useState, useRef } from "react";
import axios from "axios";
import { Autocomplete, Button, TextField, Box } from "@mui/material";
import getCookie from "../utils/GetCookie";
import Userfront from "@userfront/react";

// ag-grid
import { AgGridReact } from "ag-grid-react";

// css
import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-alpine.css";
import { useMemo } from "react";

export default function DataFrame({ tables, initialFilter, dataPickerLabel, prefix }) {
	// static const variables

	const gridRef = useRef();
	const csrftoken = getCookie("csrftoken");

	const [tableName, setTablename] = useState();
	const handleChange = (event, values) => {
		setTablename(values);
	};

	const [rowData, setRowData] = useState([]);
	const [columnDefs, setColumnDefs] = useState([]);
	useEffect(() => {
		setRowData([]);
		const fetchData = async () => {
			try {
				const result = await axios(`/api/${tableName}`);
				setRowData(result.data.filter(initialFilter));
			} catch (error) {
				console.log(error);
			}
		};

		if (tableName) {
			fetchData();
			setColumnDefs([]);
		}
	}, [tableName]);

	useEffect(() => {
		const dateColumnsByTable = [
			{ table: "fol_unas", dateCol: "" },
			{ table: "fol_bevételek", dateCol: "date" },
			{ table: "fol_gls_elszámolás", dateCol: "felvetel_datuma_" },
			{ table: "fol_költségek", dateCol: "date" },
			{ table: "fol_orders", dateCol: "Order_Date" },
			{ table: "fol_product_suppliers", dateCol: "" },
			{ table: "fol_stock_aging", dateCol: "" },
			{ table: "fol_stock_report", dateCol: "" },
			{ table: "fol_stock_transaction_report", dateCol: "Finished" },
			{ table: "fol_számlák", dateCol: "date" },
			{ table: "pro_bevételek", dateCol: "date" },
			{ table: "pro_költségek", dateCol: "date" },
			{ table: "pro_orders", dateCol: "Order_Date" },
			{ table: "pro_product_suppliers", dateCol: "" },
			{ table: "pro_stock_aging", dateCol: "" },
			{ table: "pro_stock_report", dateCol: "" },
			{ table: "pro_stock_transaction_report", dateCol: "Finished" },
			{ table: "pro_számlák", dateCol: "Date" },
		];
		let dateColumn = dateColumnsByTable.filter(({ table }) => table === tableName);
		dateColumn = dateColumn.map((table) => table.dateCol);
		for (let columnName in rowData[0]) {
			if (columnName === Object.keys(rowData[0])[0]) {
				setColumnDefs((prev) => [...prev, { field: columnName, checkboxSelection: true }]);
			} else if (columnName === dateColumn.toString()) {
				setColumnDefs((prev) => [...prev, { field: columnName, filter: "agDateColumnFilter" }]);
			} else {
				setColumnDefs((prev) => [...prev, { field: columnName }]);
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
				id='table'
				options={tables}
				sx={{ width: 300 }}
				renderInput={(params) => <TextField {...params} label={dataPickerLabel} />}
				onChange={handleChange}
				renderOption={(props, option) => (
					<Box component='li' sx={{ "& > img": { mr: 2, flexShrink: 0 } }} {...props}>
						{prefix ? option.slice(4) : option}
					</Box>
				)}
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
