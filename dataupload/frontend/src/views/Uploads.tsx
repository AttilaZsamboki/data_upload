import * as React from "react";
import axios from "axios";
import { AgGridReact } from "ag-grid-react";
import { Button } from "@mui/material";
import Userfront from "@userfront/react";
import { Navigate } from "react-router-dom";
import getCookie from "../utils/GetCookie";

import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-material.css";

interface uploadmodel {
	id: number;
	table: string;
	file: string;
	is_new_table: boolean;
	user_id: number;
	status_description: string;
	status: string;
	skiprows: number | undefined;
	upload_timestamp: Date;
}

function StatusRenderer(props: any) {
	let image;
	let style;
	switch (props.value) {
		case "error":
			image = "close.png";
			style = { width: 20, height: "auto", display: "inline-block", verticalAlign: "0%", margin: "auto" };
			break;
		case "ready":
			image = "time-left.png";
			style = { width: 20, height: "auto", display: "inline-block", verticalAlign: "0%", margin: "auto" };
			break;
		case "under upload":
			image = "engineering.png";
			style = { width: 30, height: "auto", display: "inline-block", verticalAlign: "-5%", margin: "auto" };
			break;
		case "waiting for processing":
			image = "noun-unpublished-3644027.png";
			style = { width: 30, height: "auto", display: "inline-block", verticalAlign: "-5%", margin: "auto" };
			break;
		case "success":
			image = "checked.png";
			style = { width: 30, height: "auto", display: "inline-block", verticalAlign: "-5%", margin: "auto" };
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
	if (!Userfront.accessToken()) return <Navigate to='/login' />;
	const gridRef = React.useRef();
	const [uploads, setUploads] = React.useState(null);
	React.useEffect(() => {
		const tablePrefix = Userfront.user.name.slice(0, 3) + "_";
		const fetchData = async () => {
			const response = await axios.get("/api/uploadmodel");
			return setUploads(response.data.filter((upload) => upload.table.slice(0, 4) === tablePrefix.toLowerCase()));
		};
		fetchData();
	}, []);
	const [columnDefs] = React.useState([
		{ field: "id", headerCheckboxSelection: true, checkboxSelection: true, showDisabledCheckboxes: true },
		{ field: "upload_timestamp" },
		{
			field: "table",
			cellRenderer: (params) => {
				if (params.value) {
					return params.value.slice(4);
				}
			},
		},
		{
			field: "file",
			cellRenderer: (params) => {
				if (params.value) {
					return params.value.slice(46);
				}
			},
			width: 400,
		},
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
		const csrftoken = getCookie("csrftoken");
		gridRef.current.api.applyTransaction({ remove: selectedRowData });
		selectedRowData.forEach((element: uploadmodel) => {
			const removeSocket = new WebSocket(`wss://${window.location.host}/ws/delete-upload/${element.id}/`);
			removeSocket.onmessage = function (e) {
				const data = JSON.parse(e.data);
				console.log(data);
			};
			if (element.status !== "waiting for processing") {
				axios.delete(`/api/uploadmodel/${element.id}`, {
					headers: {
						"X-CSRFToken": csrftoken && csrftoken,
						"Content-Type": "multipart/form-data",
					},
				});
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
