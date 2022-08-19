import React, { useState } from "react";
import { Navigate } from "react-router-dom";
import { FormControl, Input, InputLabel } from "@mui/material";
import KeyboardArrowUpIcon from "@mui/icons-material/KeyboardArrowUp";
import Button from "@mui/material/Button";
import Userfront from "@userfront/react";
import { Autocomplete, TextField } from "@mui/material";
import { useColumnNames, useCreateTemplate } from "../hooks/Templates";
import { useTableOptions } from "../hooks/Tables";

export default function AddTemplate() {
	if (!Userfront.accessToken()) return <Navigate to='/login' replace={true} />;
	const appendOptions = ["Hozzáfűzés duplikációk szűrésével", "Hozzáfűzés", "Felülírás"];
	const formatOptions = ["xlsx", "csv", "tsv"];
	const tableOptions = useTableOptions();
	const [state, setState] = useState({});
	const columnNames = useColumnNames(state.table);
	const { mutate: addTemplate, isSuccess } = useCreateTemplate();

	const handleChange = ({ target }) => {
		const { name, value } = target;
		setState((values) => ({ ...values, [name]: value }));
	};

	const handleAddTemplate = () => {
		// addTemplate({
		// 	table: state.table,
		// 	pkey_col: state.pkey_col,
		// 	skiprows: state.skiprows,
		// 	created_by_id: Userfront.user.userId,
		// 	append: state.append,
		// 	extension_format: state.extension_format,
		// 	source_column_names: state.source_column_names,
		// });
		console.log({ state });
	};

	return (
		<div>
			<Autocomplete
				disablePortal
				value={state.table}
				id='table'
				options={tableOptions.data}
				sx={{ width: 300 }}
				renderInput={(params) => <TextField {...params} label='Tábla neve' />}
				onChange={(e, v) => setState((prev) => ({ ...prev, table: v }))}
			/>
			<br />
			<TextField
				type='number'
				name='skiprows'
				label='Kihagyott sorok száma'
				value={state.skiprows}
				onChange={handleChange}
			/>
			<br />
			<FormControl>
				<InputLabel htmlFor='primaryKeyColumn'>Primary Key Column</InputLabel>
				<Input
					id='primaryKeyColumn'
					name='primaryKeyColumn'
					type='text'
					value={state.pkey_col}
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
				onChange={(e, v) => setState((prev) => ({ ...prev, append: v }))}
				value={state.append}
			/>
			<br />
			<Autocomplete
				disablePortal
				id='format'
				options={formatOptions}
				sx={{ width: 300 }}
				renderInput={(params) => <TextField {...params} label='Fájlformátum' />}
				onChange={(e, v) => setState((prev) => ({ ...prev, extension_format: v }))}
				value={state.extension_format}
			/>
			<br />
			{columnNames && (
				<div>
					{columnNames.data.map((column) => (
						<FormControl>
							<InputLabel htmlFor={column}>{column}</InputLabel>
							<Input id={column} name={column} type='text' onChange={handleChange} />
						</FormControl>
					))}
				</div>
			)}
			<Button
				onClick={handleAddTemplate}
				disabled={!columnNames}
				variant='contained'
				sx={{
					"backgroundColor": "#057D55",
					"&:hover": { color: "white" },
				}}
				endIcon={<KeyboardArrowUpIcon />}
				type='submit'>
				Submit
			</Button>
			{isSuccess && <Navigate to='/upload' replace={true} />}
		</div>
	);
}
