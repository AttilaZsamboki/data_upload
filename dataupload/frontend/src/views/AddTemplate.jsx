import React, { useState, useEffect } from "react";
import { Navigate } from "react-router-dom";
import { FormControl, FormControlLabel, Input, InputLabel } from "@mui/material";
import KeyboardArrowUpIcon from "@mui/icons-material/KeyboardArrowUp";
import Button from "@mui/material/Button";
import Userfront from "@userfront/react";
import getCookie from "../utils/GetCookie";
import { Autocomplete, TextField } from "@mui/material";
import { event } from "jquery";

export default function AddConnection() {
	const csrftoken = getCookie("csrftoken");
	const appendOptions = ["Hozzáfűzés duplikációk szűrésével", "Hozzáfűzés", "Felülírás"];
	const [appendOption, setAppendOption] = useState(null);
	const [tables, setTables] = useState([]);
	const [table, setTable] = useState(null);
	const [isFinished, setisFinished] = useState(false);
	const [inputs, setInputs] = useState({
		primaryKeyColumn: "",
		skiprows: "",
		extensionFormat: "",
	});

	useEffect(() => {
		const tablePrefix = Userfront.user.name.slice(0, 3) + "_";
		fetch("/api/table-names")
			.then((response) => response.json())
			.then((json) =>
				setTables(json.filter((table) => table.slice(0, 4).toLowerCase() === tablePrefix.toLowerCase()))
			);
	}, []);

	const handleChange = (event) => {
		const name = event.target.name;
		const value = event.target.value;
		setInputs((values) => ({ ...values, [name]: value }));
	};

	async function handleSubmit(event) {
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
				table: table,
				pkey_col: inputs.primaryKeyColumn,
				skiprows: inputs.skiprows,
				created_by_id: Userfront.user.userId,
				append: appendOption,
				extension_format: inputs.extensionFormat,
			}),
		};
		try {
			const response = await fetch("/api/templates.json", requestOptions);
			const json = await response.json();
			console.log(json);
			setisFinished(true);
		} catch (error) {
			console.log(error);
		}
	}

	const formControlStyle = {
		marginBottom: 20,
		width: 500,
	};

	return (
		<form onSubmit={handleSubmit}>
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
				<InputLabel htmlFor='skiprows'>Number of rows to skip</InputLabel>
				<Input id='skiprows' name='skiprows' type='skiprows' value={inputs.skiprows} onChange={handleChange} />
			</FormControl>
			<br />
			<FormControl style={formControlStyle}>
				<InputLabel htmlFor='primaryKeyColumn'>Primary Key Column</InputLabel>
				<Input
					id='primaryKeyColumn'
					name='primaryKeyColumn'
					type='text'
					value={inputs.pkey_col}
					onChange={handleChange}
				/>
			</FormControl>
			<br />
			<Autocomplete
				disablePortal
				id='appendOptions'
				name='appendOptions'
				type='text'
				options={appendOptions}
				sx={{ width: 300 }}
				renderInput={(params) => <TextField {...params} label='Hozááfűzés formája' />}
				onChange={(event, values) => setAppendOption(values)}
				value={appendOption}
			/>
			<br />
			<FormControl style={formControlStyle}>
				<InputLabel htmlFor='extensionFormat'>Extension Format</InputLabel>
				<Input
					id='extensionFormat'
					name='extensionFormat'
					type='text'
					value={inputs.extensionFormat}
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
			{/* {isFinished && <Navigate to='/upload' replace={true} />} */}
		</form>
	);
}