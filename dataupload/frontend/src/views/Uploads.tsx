import * as React from "react";
import axios from "axios";
import { AgGridReact } from "ag-grid-react";
import { Button, CircularProgress } from "@mui/material";
import Userfront from "@userfront/react";
import { Navigate } from "react-router-dom";
import formatDate from "../utils/date";
import { useUsersData } from "../hooks/users";
import { useTableOptionsAll } from "../hooks/Tables";

import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-material.css";

const fileDownload = require("js-file-download");

interface uploadmodel {
	id: number;
	table: string;
	file: string;
	is_new_table: boolean;
	user_id: number;
	status_description: string;
	status: string;
	upload_timestamp: Date;
}

function StatusRenderer(props: any) {
	let image;
	let style;
	switch (props.value) {
		case "error":
			image = "close.png";
			style = { width: 30, height: "auto", display: "inline-block", verticalAlign: "0%", margin: "auto" };
			break;
		case "ready":
			image = "time-left.png";
			style = { width: 30, height: "auto", display: "inline-block", verticalAlign: "0%", margin: "auto" };
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

function ModeRenderer(props: any) {
	let image;
	let style;
	switch (props.value) {
		case "Email":
			image = "email.png";
			style = { width: 30, height: "auto", display: "inline-block", verticalAlign: "0%", margin: "auto" };
			break;
		case "Kézi":
			image = "settings.png";
			style = { width: 30, height: "auto", display: "inline-block", verticalAlign: "-10%", margin: "auto" };
			break;
		case "Feed":
			image = "animal-feed.png";
			style = { width: 30, height: "auto", display: "inline-block", verticalAlign: "-5%", margin: "auto" };
			break;
		default:
			image = "question-mark.png";
			style = { width: 30, height: "auto", display: "inline-block", margin: "auto" };
			break;
	}
	const imageSource = `../../static/images/${image}`;
	return (
		<span className='text-center'>
			<img src={imageSource} style={style} />
			<p style={{ paddingLeft: 3, display: "inline-block", verticalAlign: "middle", marginLeft: 10 }}>
				{props.value}
			</p>
		</span>
	);
}

function FileRenderer(props: any) {
	const [downloading, setDownloading] = React.useState(false);
	const path = props.value.replace("http://127.0.0.1:8000/media", "");
	const downloadFile = async () => {
		if (downloading) {
			setDownloading(false);
			return false;
		}
		setDownloading(true);
		const response = await axios(`/api/download-log?path=${props.data.table}/${path}`, { responseType: "blob" });
		fileDownload(response.data, `${props.data.file.split("/").at(-1)}`);
		setDownloading(false);
	};
	return (
		<div>
			{downloading ? (
				<button onClick={downloadFile}>
					<CircularProgress style={{ width: 30 }} />
				</button>
			) : (
				<button onClick={downloadFile}>{path}</button>
			)}
		</div>
	);
}

export default function Uploads() {
	const tableOverview = useTableOptionsAll();
	const tableGetter = (params) => {
		if (params.data.table && tableOverview.isFetched) {
			return tableOverview.data?.find((element) => element.db_table === params.data.table)?.verbose_name;
		}
	};
	if (!Userfront.accessToken()) return <Navigate to='/login' />;
	const gridRef = React.useRef();
	const userData = useUsersData();
	const [uploads, setUploads] = React.useState(null);
	React.useEffect(() => {
		const tablePrefix = Userfront.user.name.slice(0, 3) + "_";
		const fetchData = async () => {
			const response = await axios.get("/api/uploadmodel");
			if (["dark-frost-2k269", "winter-salad-brlnr", "ancient-river-26kn4"].includes(Userfront.user.username))
				return setUploads(response.data);
			return setUploads(response.data.filter((upload) => upload.table.slice(0, 4) === tablePrefix.toLowerCase()));
		};
		fetchData();
	}, []);
	const [columnDefs, setColumnDefs] = React.useState([
		{
			field: "id",
			headerCheckboxSelection: true,
			checkboxSelection: true,
			headerName: "Azonosító",
		},
		{
			field: "upload_timestamp",
			cellRenderer: (params) => {
				if (params.value) {
					return formatDate(new Date(params.value));
				}
			},
			headerName: "Feltöltés ideje",
			initialSort: "desc",
			filter: "agDateColumnFilter",
		},
		{
			field: "file",
			valueGetter: (params) => {
				return params.data.file.split("/").at(-1);
			},
			cellRendererSelector: () => {
				return {
					component: FileRenderer,
				};
			},
			width: 400,
			headerName: "Fájl",
		},
		{
			field: "status",
			cellRendererSelector: () => {
				return {
					component: StatusRenderer,
				};
			},
			headerName: "Státusz",
		},
		{
			field: "mode",
			cellRendererSelector: () => {
				return {
					component: ModeRenderer,
				};
			},
			headerName: "Mód",
		},
	]);
	React.useEffect(() => {
		if (
			["dark-frost-2k269", "winter-salad-brlnr", "ancient-river-26kn4"].includes(Userfront.user.username) &&
			userData.isFetched &&
			gridRef.current.api
		) {
			gridRef.current.api.setColumnDefs([
				...columnDefs,
				{
					headerName: "Tulajdonos",
					valueGetter: (params) => {
						if (params.data.user_id && userData.isFetched) {
							return userData.data?.results.find((element) => element.userId === params.data.user_id)
								.name;
						}
					},
				},
			]);
		}
	}, [userData.isFetched]);
	React.useEffect(() => {
		if (!tableOverview.isLoading) {
			const [x, y, ...z] = columnDefs;
			setColumnDefs((prev) => [
				x,
				y,
				{
					field: "table",
					valueGetter: tableGetter,
					headerName: "Tábla",
					colId: "table",
				},
				...z,
			]);
		}
	}, [tableOverview.status]);

	const defaultColDef = React.useMemo(
		() => ({
			floatingFilter: true,
			filter: true,
			sortable: true,
			resizable: true,
			flex: 1,
			filterParams: {
				debounceMs: 0,
			},
		}),
		[]
	);
	const onRemoveSelected = () => {
		const selectedRowData = gridRef.current.api.getSelectedRows();
		gridRef.current.api.applyTransaction({ remove: selectedRowData });
		selectedRowData.forEach((element: uploadmodel) => {
			if (element.status !== "waiting for processing") {
				const removeSocket = new WebSocket(`wss://${window.location.host}/ws/delete-upload/${element.id}/`);
			}
		});
	};
	return (
		<div className='mx-auto flex flex-col items-center justify-center'>
			<h1 className='mb-5'>Feltöltések</h1>
			<Button variant='outlined' onClick={onRemoveSelected}>
				Feltöltés törlése
			</Button>
			<p className='text-xs mt-3'>Nem lehetséges miután a fájl feldolgozásra került</p>
			<div className='ag-theme-material' style={{ height: 700, width: "80%" }}>
				<AgGridReact
					ref={gridRef}
					rowData={uploads}
					columnDefs={columnDefs}
					animateRows={true}
					rowSelection={"multiple"}
					defaultColDef={defaultColDef}
					pagination={true}
					paginationAutoPageSize={true}
				/>
			</div>
		</div>
	);
}