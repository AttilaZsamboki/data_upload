import React, { useState } from "react";
import {
	FormControl,
	FormControlLabel,
	Input,
	InputLabel,
} from "@mui/material";
import KeyboardArrowUpIcon from "@mui/icons-material/KeyboardArrowUp";
import Button from "@mui/material/Button";
import Userfront from "@userfront/react";
import getCookie from "../utils/GetCookie";
import Checkbox from "@mui/material/Checkbox";

export default function AddConnection() {
	const csrftoken = getCookie("csrftoken");
	const [inputs, setInputs] = useState({
		table: "",
		primaryKeyColumn: "",
		skiprows: "",
		isAppend: true,
		extensionFormat: "",
	});

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
				Accept: "application/json",
				"X-CSRFToken": csrftoken,
				"Content-Type": "application/json",
			},
			body: JSON.stringify({
				table: inputs.table,
				pkey_col: inputs.primaryKeyColumn,
				skiprows: inputs.skiprows,
				created_by_id: Userfront.user.userId,
				append: inputs.isAppend,
				extension_format: inputs.extensionFormat,
			}),
		};
		fetch("/api/templates.json", requestOptions)
			.then((response) => response.json)
			.then((data) => console.log(data))
			.catch((error) => console.log(error));
		setInputs({
			table: "",
			pkey_col: "",
			skiprows: "",
			created_by_id: "",
			append: "",
			extension_format: "",
		});
	};

	const formControlStyle = {
		marginBottom: 20,
		width: 500,
	};

	const label = { inputProps: { "aria-label": "Checkbox demo" } };

	return (
		<form onSubmit={handleSubmit}>
			<FormControl style={formControlStyle}>
				<InputLabel htmlFor='table'>Table</InputLabel>
				<Input
					id='table'
					name='table'
					type='text'
					value={inputs.table}
					onChange={handleChange}
				/>
			</FormControl>
			<br />
			<FormControl style={formControlStyle}>
				<InputLabel htmlFor='skiprows'>
					Number of rows to skip
				</InputLabel>
				<Input
					id='skiprows'
					name='skiprows'
					type='skiprows'
					value={inputs.skiprows}
					onChange={handleChange}
				/>
			</FormControl>
			<br />
			<FormControl style={formControlStyle}>
				<InputLabel htmlFor='primaryKeyColumn'>
					Primary Key Column
				</InputLabel>
				<Input
					id='primaryKeyColumn'
					name='primaryKeyColumn'
					type='text'
					value={inputs.pkey_col}
					onChange={handleChange}
				/>
			</FormControl>
			<br />
			<FormControlLabel
				control={
					<Checkbox
						{...label}
						defaultChecked
						id='isAppend'
						name='isAppend'
						value={inputs.isAppend}
						onClick={(event) =>
							setInputs((values) => ({
								...values,
								append: event.target.checked,
							}))
						}
					/>
				}
				label='Should uploads be appended'
				labelPlacement='top'
			/>
			<br />
			<FormControl style={formControlStyle}>
				<InputLabel htmlFor='extensionFormat'>
					Extension Format
				</InputLabel>
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
					backgroundColor: "#057D55",
					"&:hover": { color: "white" },
				}}
				endIcon={<KeyboardArrowUpIcon />}
				type='submit' /*href='/templates'*/
			>
				Submit
			</Button>
		</form>
	);
}
