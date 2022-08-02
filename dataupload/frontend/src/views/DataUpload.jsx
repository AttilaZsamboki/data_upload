import React, { useState, useEffect } from "react";
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
	const csrftoken = getCookie("csrftoken");
	const [tableOptions, setTablesOptions] = useState([]);
	const [inputTable, setInputTable] = useState("");
	const [selectedFile, setSelectedFile] = useState(null);

	useEffect(() => {
		const fetchData = async () => {
			const data = await fetch("/api/templates");
			const json = await data.json();
			setTablesOptions(
				json
					.filter(
						(res) => res.created_by_id === Userfront.user.userId
					)
					.map((res) => res.table)
			);
			return json;
		};

		fetchData();
	}, []);

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
					renderInput={(params) => (
						<TextField {...params} label='Template neve' />
					)}
					onChange={handleChange}
				/>
				<br />
				<FormControl style={formControlStyle}>
					<input
						id='file'
						name='file'
						type='file'
						onChange={onFileChange}
					/>
				</FormControl>
				<br />
				<Button
					variant='contained'
					sx={{
						backgroundColor: "#057D55",
						"&:hover": { color: "white" },
					}}
					href='/upload'
					endIcon={<FileUploadIcon />}
					type='text'>
					Upload
				</Button>
			</form>
		</div>
	);
}
