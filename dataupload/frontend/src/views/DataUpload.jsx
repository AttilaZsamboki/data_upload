import React, { useState, useEffect, useRef } from "react";
import Userfront from "@userfront/react";
import { Navigate } from "react-router-dom";
import { Autocomplete } from "@mui/material";
import getCookie from "../utils/GetCookie";
import FileUploadIcon from "@mui/icons-material/FileUpload";
import CloseIcon from "@mui/icons-material/Close";
import { FormControl, TextField, Alert, Box, Collapse, Button } from "@mui/material";
import IconButton from "@mui/material/IconButton";
import axios from "axios";

export default function SpecialQueries() {
	if (!Userfront.accessToken()) {
		return <Navigate to='/login' />;
	}
	const inputRef = useRef(null);
	const csrftoken = getCookie("csrftoken");
	const [tableOptions, setTablesOptions] = useState([]);
	const [inputTable, setInputTable] = useState(null);
	const [selectedFile, setSelectedFile] = useState(null);
	const [minDate, setMinDate] = useState(null);
	const [maxDate, setMaxDate] = useState(null);
	const [isLoadingDate, setIsLoadingDate] = useState(true);
	const [error, setError] = useState(null);

	useEffect(() => {
		const tablePrefix = Userfront.user.name.slice(0, 3) + "_";
		const fetchTables = async () => {
			const data = await fetch("/api/templates");
			const json = await data.json();
			setTablesOptions(
				json
					.filter((res) => res.table.slice(0, 4).toLowerCase() === tablePrefix.toLowerCase())
					.map((res) => res.table)
			);
			return json;
		};

		fetchTables();
		document.title = "Upload";
	}, []);


	useEffect(() => {
		setIsLoadingDate(true);
		setMinDate(null);
		setMaxDate(null);
		const fetchData = async () => {
			const data = await fetch(`/api/${inputTable}`);
			const json = await data.json();
			const dateColumnsByTable = [
				{ table: "fol_unas", dateCol: "" },
				{ table: "fol_bevételek", dateCol: "teljesites_datuma" },
				{ table: "fol_gls_elszámolás", dateCol: "Felvetel_datuma_" },
				{ table: "fol_költségek", dateCol: "date" },
				{ table: "fol_orders", dateCol: "Order_Date" },
				{ table: "fol_product_suppliers", dateCol: "" },
				{ table: "fol_stock_aging", dateCol: "" },
				{ table: "fol_stock_report", dateCol: "" },
				{ table: "fol_stock_transaction_report", dateCol: "Finished" },
				{ table: "fol_számlák", dateCol: "Date" },
				{ table: "pro_bevételek", dateCol: "date" },
				{ table: "pro_költségek", dateCol: "date" },
				{ table: "pro_orders", dateCol: "Order_Date" },
				{ table: "pro_product_suppliers", dateCol: "" },
				{ table: "pro_stock_aging", dateCol: "" },
				{ table: "pro_stock_report", dateCol: "" },
				{ table: "pro_stock_transaction_report", dateCol: "Finished" },
				{ table: "pro_számlák", dateCol: "Date" },
			];
			let dateColumn = dateColumnsByTable.filter(({ table, dateCol }) => table === inputTable && dateCol);
			dateColumn = dateColumn.map((table) => table.dateCol);
			const maxDateJson = dateColumn
				? new Date(
						Math.max(
							...json.map((element) => {
								return new Date(element[dateColumn]);
							})
						)
				  )
				: "";
			const minDateJson = dateColumn
				? new Date(
						Math.min(
							...json.map((element) => {
								return new Date(element[dateColumn]);
							})
						)
				  )
				: "";
			setMinDate(minDateJson);
			setMaxDate(maxDateJson);
			setIsLoadingDate(false);
		};

		inputTable && fetchData();
	}, [inputTable]);

	const onFileChange = (e) => {
		setSelectedFile(e.target.files[0]);
	};

	const handleChange = (event, values) => {
		setInputTable(values);
	};

	const onFileUpload = (event) => {
		event.preventDefault();
		if (inputTable && selectedFile) {
			const formData = new FormData();
			formData.append("table", inputTable);
			formData.append("file", selectedFile);
			formData.append("user_id", Userfront.user.userId);
			formData.append("is_new_table", false);
			axios({
				method: "post",
				url: "/api/uploadmodel/",
				data: formData,
				headers: {
					"X-CSRFToken": csrftoken,
					"Content-Type": "multipart/form-data",
				},
			});
			setInputTable(null);
			inputRef.current.value = null;
		} else if (!inputTable) {
			setError("Válassz ki egy táblát a feltöltéshez");
		} else if (!selectedFile) {
			setError("Adj meg egy fájlt a feltöltéshez");
			console.log(inputTable);
		}
	};

	const formControlStyle = {
		marginBottom: 20,
		width: 500,
	};

	return (
		<div>
			{error && (
				<Box sx={{ width: "100%" }}>
					<Collapse in={error}>
						<Alert
							severity='warning'
							action={
								<IconButton
									aria-label='close'
									color='inherit'
									size='small'
									onClick={() => {
										setError(null);
									}}>
									<CloseIcon fontSize='inherit' />
								</IconButton>
							}
							sx={{ mb: 2 }}>
							{error}
						</Alert>
					</Collapse>
				</Box>
			)}
			<form onSubmit={onFileUpload}>
				<Autocomplete
					disablePortal
					id='table'
					name='table'
					type='text'
					options={tableOptions}
					sx={{ width: 300 }}
					renderInput={(params) => <TextField {...params} label='Tábla neve' />}
					onChange={handleChange}
					value={inputTable && inputTable.replace((Userfront.user.name.slice(0, 3) + "_").toLowerCase(), "")}
					renderOption={(props, option) => (
						<Box component='li' sx={{ "& > img": { mr: 2, flexShrink: 0 } }} {...props}>
							{option.replace((Userfront.user.name.slice(0, 3) + "_").toLowerCase(), "")}
						</Box>
					)}
				/>
				<br />
				{!isLoadingDate && (
					<div>
						<p>
							Adathalmaz kezdete:{" "}
							{minDate.toLocaleString("hu-HU", { year: "numeric", month: "2-digit", day: "2-digit" })}
						</p>{" "}
						<br />
						<p>
							Adathalmaz vége:{" "}
							{maxDate.toLocaleString("hu-HU", { year: "numeric", month: "2-digit", day: "2-digit" })}
						</p>
					</div>
				)}
				<FormControl style={formControlStyle}>
					<input id='file' name='file' type='file' onChange={onFileChange} ref={inputRef} />
				</FormControl>
				<br />
				<Button
					variant='contained'
					sx={{
						"backgroundColor": "#057D55",
						"&:hover": { color: "white" },
					}}
					endIcon={<FileUploadIcon />}
					type='submit'>
					Upload
				</Button>
			</form>
		</div>
	);
}
