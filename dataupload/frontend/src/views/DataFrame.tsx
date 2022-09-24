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
import { useColumnDtypes } from "../hooks/Templates";
import { useGroupTables } from "../hooks/users";

const csrftoken = getCookie("csrftoken");

interface tableOverview {
	db_table: string;
	available_at: string;
	verbose_name: string;
}


function DataFrame({ importConfig }: { importConfig: boolean }) {
	const gridRef = React.useRef();
	const [inputTable, setInputTable] = useState<string>();
	const [columnDefs, setColumnDefs] = useState(null);
	const tableOverview = useTableOptions().data;
	const groupTables = useGroupTables();
	const tableOptions =
		tableOverview &&
		tableOverview
			.filter(
				(table: tableOverview) =>
					table.available_at.includes("grid") && groupTables.data?.includes(table.db_table)
			)
			.map((table: tableOverview) => table.verbose_name);
	const formattedInputTable = !importConfig
		? tableOverview &&
		  tableOverview
				.filter(
					(table: tableOverview) =>
						table.verbose_name === inputTable && groupTables.data?.includes(table.db_table)
				)
				.map((table: tableOverview) => table.db_table)
				.toString()
		: inputTable?.replace(" ", "-").toLowerCase();
	const table: any = useTable(formattedInputTable);
	const importConfigTypes = ["Templates", "Table Overview", "Feed"];
	const columnNames = useColumnDtypes(formattedInputTable);

	useEffect(() => {
		if (table.data && table.data.length && inputTable) {
			setColumnDefs(
				Object.keys(table.data[0]).map((col) =>
					columnNames.data?.filter((element) => element[1] === "date").find((element) => element[0] === col)
						? {
								field: col,
								filter: "agDateColumnFilter",
								filterParams: {
									// provide comparator function
									comparator: (filterLocalDateAtMidnight, cellValue) => {
										const dateAsString = cellValue;

										if (dateAsString == null) {
											return 0;
										}

										// In the example application, dates are stored as dd/mm/yyyy
										// We create a Date object for comparison against the filter date
										const dateParts = dateAsString.split("-");
										const year = Number(dateParts[0]);
										const month = Number(dateParts[1]) - 1;
										const day = Number(dateParts[2]);
										const cellDate = new Date(year, month, day);

										// Now that both parameters are Date objects, we can compare
										if (cellDate < filterLocalDateAtMidnight) {
											return -1;
										} else if (cellDate > filterLocalDateAtMidnight) {
											return 1;
										}
										return 0;
									},
								},
						  }
						: Object.keys(table.data[0]).indexOf(col) === 0 && importConfig
						? { field: col, floatingFilter: true, headerCheckboxSelection: true, checkboxSelection: true }
						: { field: col, floatingFilter: true }
				)
			);
		}
	}, [inputTable, table]);

	const defaultColDef = useMemo(
		() => ({
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
	const onRemoveSelected = async () => {
		const selectedRowData = gridRef.current.api.getSelectedRows();
		gridRef.current.api.applyTransaction({ remove: selectedRowData });
		await selectedRowData.forEach((element: uploadmodel) => {
			axios.delete(`/api/${formattedInputTable}/${element.id}`, {
				headers: {
					"X-CSRFToken": csrftoken,
				},
			});
		});
	};
	return (
		<div>
			<h1 className='flex flex-col items-center justify-center mb-5'>
				{!importConfig ? "Adatok" : "Import Konfigurációk"}
			</h1>
			<Autocomplete
				className='m-auto flex flex-col items-center justify-center'
				id='table'
				options={importConfig ? importConfigTypes : tableOptions}
				sx={{ width: 300 }}
				renderInput={(params) => <TextField {...params} label={importConfig ? "Konfig neve" : "Tábla neve"} />}
				onChange={(e, v) => setInputTable(v)}
			/>
			{importConfig && (
				<Box textAlign='center' marginTop={5}>
					<Button
						sx={{
							"&:hover": { color: "white" },
							"backgroundColor": "#057D55",
							"marginBottom": 4,
						}}
						variant='contained'
						href={`/add-${inputTable?.toLowerCase().replace(" ", "-")}`}
						disabled={!inputTable}>
						{inputTable} hozzáadása
					</Button>
					<br />
					<Button
						variant='outlined'
						onClick={onRemoveSelected}
						disabled={!gridRef.current?.api?.getSelectedRows().length}>
						Template törlése
					</Button>
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
						stopEditingWhenCellsLoseFocus={true}
						onCellValueChanged={onBtWhich}
						pagination={true}
						paginationAutoPageSize={true}
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
