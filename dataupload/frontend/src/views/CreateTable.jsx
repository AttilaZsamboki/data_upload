import React, { useState, useEffect, useRef } from "react";
import Userfront from "@userfront/react";
import { Navigate } from "react-router-dom";
import getCookie from "../utils/GetCookie";
import AddIcon from "@mui/icons-material/Add";
import { FormControl, Input, InputLabel, Button, FormHelperText } from "@mui/material";
import axios from "axios";

export default function SpecialQueries() {
	if (!Userfront.accessToken()) {
		return <Navigate to='/login' />;
	}
	const inputRef = useRef(null);
	const csrftoken = getCookie("csrftoken");
	const [inputTable, setInputTable] = useState(null);
	const [selectedFile, setSelectedFile] = useState(null);

	const onFileChange = (e) => {
		setSelectedFile(e.target.files[0]);
	};

	const handleChange = ({ target }) => {
		setInputTable(target.value);
	};

	const onFileUpload = (event) => {
		const tablePrefix = Userfront.user.name.toLowerCase().slice(0, 3) + "_";
		event.preventDefault();
		const formData = new FormData();
		formData.append("table", tablePrefix + inputTable);
		formData.append("file", selectedFile);
		formData.append("user_id", Userfront.user.userId);
		formData.append("is_new_table", true);
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
		width: 200,
	};

	return (
		<div>
			<form onSubmit={onFileUpload}>
				<FormControl style={formControlStyle}>
					<InputLabel htmlFor='table'>Tábla neve</InputLabel>
					<Input id='table' name='table' type='text' value={inputTable} onChange={handleChange} />
				</FormControl>
				<br />
				<FormControl style={formControlStyle}>
					<input id='file' name='file' type='file' onChange={onFileChange} ref={inputRef} />
					<FormHelperText>Példa File</FormHelperText>
				</FormControl>
				<br />
				<Button
					variant='contained'
					sx={{
						"backgroundColor": "#057D55",
						"&:hover": { color: "white" },
					}}
					endIcon={<AddIcon />}
					type='submit'>
					Létrehozás
				</Button>
			</form>
		</div>
	);
}
