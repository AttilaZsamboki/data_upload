import React, { useState, useEffect, useRef } from "react";
import Userfront from "@userfront/react";
import { Navigate } from "react-router-dom";
import { Autocomplete } from "@mui/material";
import getCookie from "../utils/GetCookie";
import FileUploadIcon from "@mui/icons-material/FileUpload";
import Button from "@mui/material/Button";
import { FormControl, Input, InputLabel, TextField } from "@mui/material";
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

	useEffect(() => {
		const fetchTables = async () => {
			const data = await fetch("/api/templates");
			const json = await data.json();
			setTablesOptions(json.filter((res) => res.created_by_id === Userfront.user.userId).map((res) => res.table));
			return json;
		};

		fetchTables();
	}, []);

	useEffect(() => {
		const fetchData = async () => {
			const data = await fetch(`/api/${inputTable}`);
			const json = await data.json();
			const maxDateJson = new Date(
				Math.max(
					...json.map((element) => {
						return new Date(element.date);
					})
				)
			);
			const minDateJson = new Date(
				Math.min(
					...json.map((element) => {
						return new Date(element.date);
					})
				)
			);
			setMinDate(minDateJson);
			setMaxDate(maxDateJson);
			setIsLoadingDate(false);
		};

		fetchData();
	}, [inputTable]);

	const onFileChange = (e) => {
		setSelectedFile(e.target.files[0]);
	};

	const handleChange = (event, values) => {
		setInputTable(values);
	};

	const onFileUpload = (event) => {
		event.preventDefault();
		const formData = new FormData();
		formData.append("table", inputTable);
		formData.append("file", selectedFile);
		formData.append("user_id", Userfront.user.userId);
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
	};

	const formControlStyle = {
		marginBottom: 20,
		width: 500,
	};

	return (
		<div>
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
					value={inputTable}
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
