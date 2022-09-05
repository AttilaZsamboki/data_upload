import * as React from "react";
import axios from "axios";
import { useQuery } from "react-query";
import { AgGridReact } from "ag-grid-react";
import { Button } from "@mui/material";

import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-material.css";

interface uploadmodel {
	id: number;
	table: string;
	file: string;
	is_new_table: boolean;
	user_id: number;
	timestamp: string;
	status_description: string;
	status: string;
	skiprows: number | undefined;
}

function StatusRenderer(props: any) {
	let image;
	let style;
	switch (props.value) {
		case "error":
			image = "close.png";
			style = { width: 20, height: "auto", display: "inline-block", verticalAlign: "0%", margin: "auto" };
			break;
		case "waiting":
			image = "time-left.png";
			style = { width: 20, height: "auto", display: "inline-block", verticalAlign: "0%", margin: "auto" };
			break;
		case "under upload":
			image = "engineering.png";
			style = { width: 30, height: "auto", display: "inline-block", verticalAlign: "-5%", margin: "auto" };
			break;
	}
	const imageSource = `../../static/images/${image}`;
	return (
		<span className='text-center'>
			<img src={imageSource} style={style} />
			<p style={{ paddingLeft: 3, display: "inline-block", verticalAlign: "middle", marginLeft: 10 }}>
				{props.data.status_description}
			</p>
		</span>
	);
}

export default function Uploads() {
	const gridRef = React.useRef();
	const [uploads, setUploads] = React.useState(null);
	React.useEffect(() => {
		const fetchData = async () => {
			const response = await axios.get("/api/uploadmodel");
			return setUploads(response.data);
		};
		fetchData();
	}, []);
	const [columnDefs] = React.useState([
		{ field: "id", headerCheckboxSelection: true, checkboxSelection: true, showDisabledCheckboxes: true },
		{ field: "timestamp" },
		{ field: "table" },
		{ field: "file" },
		{
			field: "status",
			flex: 1,
			editable: true,
			resizable: true,
			cellRendererSelector: () => {
				return {
					component: StatusRenderer,
				};
			},
		},
	]);
	const onRemoveSelected = () => {
		const selectedRowData = gridRef.current.api.getSelectedRows();
		selectedRowData.forEach((element: uploadmodel) => {
			if (element.status === "waiting") {
				gridRef.current.api.applyTransaction({ remove: element });
				axios.delete(`/api/uploadmodel/${element.id}`);
			}
		});
	};
	return (
		<div className='mx-auto flex flex-col items-center justify-center '>
			<h1 className='mb-5'>Feltöltések</h1>
			<Button variant='outlined' onClick={onRemoveSelected}>
				Feltöltés törlése
			</Button>
			<p className='text-xs mt-3'>Nem lehetséges miután a fájl feldolgozásra került</p>
			<div className='ag-theme-material' style={{ height: 400, width: "80%" }}>
				<AgGridReact
					ref={gridRef}
					rowData={uploads}
					columnDefs={columnDefs}
					animateRows={true}
					rowSelection={"multiple"}
				/>
			</div>
		</div>
	);
}
