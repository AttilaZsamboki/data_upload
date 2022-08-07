import React, { useState, useEffect } from "react";
import { FormControl, Input, InputLabel, Button, Autocomplete, TextField } from "@mui/material";
import KeyboardArrowUpIcon from "@mui/icons-material/KeyboardArrowUp";
import Userfront from "@userfront/react";
import getCookie from "../utils/GetCookie";

export default function AddConnection() {
	const csrftoken = getCookie("csrftoken");
	const [tables, setTables] = useState([]);

	useEffect(() => {
		const tablePrefix = Userfront.user.name.slice(0, 3) + "_";
		fetch("/api/table-names")
			.then((response) => response.json())
			.then((json) =>
				setTables(json.filter((table) => table.slice(0, 4).toLowerCase() === tablePrefix.toLowerCase()))
			);
	}, []);

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
			</FormControl>
			<br />
			<Autocomplete
				disablePortal
				id='table'
				options={tables}
				sx={{ width: 300 }}
				renderInput={(params) => <TextField {...params} label='Tábla neve' />}
				onChange={(event, values) => setTable(values)}
			/>
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
