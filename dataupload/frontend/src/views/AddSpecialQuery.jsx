import React, { useState } from "react";
import { FormControl, FormHelperText, Input, InputLabel } from "@mui/material";
import KeyboardArrowUpIcon from "@mui/icons-material/KeyboardArrowUp";
import Button from "@mui/material/Button";
import Userfront from "@userfront/react";
import getCookie from "../utils/GetCookie";

export default function AddConnection() {
	const csrftoken = getCookie("csrftoken");
	console.log(Userfront.tokens.accessToken);

	const [inputs, setInputs] = useState({});

	const handleChange = (event) => {
		const name = event.target.name;
		const value = event.target.value;
		setInputs((values) => ({ ...values, [name]: value }));
	};

	const handleSubmit = (event) => {
		event.preventDefault();
		const requestOptions = {
			credentials: "include",
			method: "POST",
			mode: "same-origin",
			headers: {
				"Accept": "application/json",
				"X-CSRFToken": csrftoken,
				"Content-Type": "application/json",
				"Authorization": `Bearer ${Userfront.tokens.accessToken}`,
			},
			body: JSON.stringify({
				name: inputs.name,
				table: inputs.table,
				special_query: inputs.special_query,
				created_by: Userfront.user.userId,
			}),
		};
		fetch("/api/special-queries/", requestOptions)
			.then((response) => response.json)
			.then((data) => console.log(data))
			.catch((error) => console.log(error));
		setInputs({ name: "", table: "", special_query: "" });
	};

	const formControlStyle = {
		marginBottom: 20,
		width: 500,
	};

	return (
		<form onSubmit={handleSubmit}>
			<FormControl style={formControlStyle}>
				<InputLabel htmlFor='name'>Query Name</InputLabel>
				<Input id='name' name='name' type='text' value={inputs.name} onChange={handleChange} />
				<FormHelperText id='name-helper'>You can choose any name for your connection.</FormHelperText>
			</FormControl>
			<br />
			<FormControl style={formControlStyle}>
				<InputLabel htmlFor='table'>Table</InputLabel>
				<Input id='table' name='table' type='text' value={inputs.table} onChange={handleChange} />
			</FormControl>
			<br />
			<FormControl style={formControlStyle}>
				<InputLabel htmlFor='special_query'>Special_query</InputLabel>
				<Input
					id='special_query'
					name='special_query'
					type='text'
					value={inputs.special_query}
					onChange={handleChange}
				/>
			</FormControl>
			<br />
			<Button
				variant='contained'
				sx={{
					"backgroundColor": "#057D55",
					"&:hover": { color: "white" },
				}}
				endIcon={<KeyboardArrowUpIcon />}
				type='submit'>
				Submit
			</Button>
		</form>
	);
}
