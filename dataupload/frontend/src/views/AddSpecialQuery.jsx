import React, { useState, useEffect } from "react";
import { Navigate } from "react-router-dom";
import { FormControl, Input, InputLabel, Button, Autocomplete, TextField } from "@mui/material";
import KeyboardArrowUpIcon from "@mui/icons-material/KeyboardArrowUp";
import Userfront from "@userfront/react";
import { useTableOptions } from "../hooks/Tables";
import useCreateSpecialQuery from "../hooks/SpecialQueries";

export default function addSpecialQueries() {
	if (!Userfront.accessToken()) return <Navigate to='/login' replace={true} />;
	const tables = useTableOptions();
	const { mutate: addSpecialQuery, isSuccess } = useCreateSpecialQuery();
	const [state, setState] = useState({});

	const handleAddSpecialQuery = () => {
		addSpecialQuery({
			special_query: state.special_query,
			created_by_id: Userfront.user.userId,
			table: state.table,
			name: state.name,
		});
	};

	if (tables.isLoading) return <span>Loading...</span>;
	if (tables.isError) return <span>Error: {tables.error.message}</span>;

	return (
		<>
			<div sx={{ marginBottom: 20, width: 500 }}>
				<FormControl>
					<InputLabel htmlFor='name'>Query Name</InputLabel>
					<Input
						id='name'
						name='name'
						type='text'
						onChange={(e) => setState((prev) => ({ ...prev, name: e.target.value }))}
						value={state.name}
					/>
				</FormControl>
				<br />
				<Autocomplete
					disablePortal
					id='table'
					options={tables.data}
					sx={{ width: 300 }}
					onChange={(e, v) => setState((prev) => ({ ...prev, table: v }))}
					value={state.table}
					renderInput={(params) => <TextField {...params} label='Tábla neve' />}
				/>
				<br />
				<TextField
					id='special-query'
					label='Special SQL query'
					multiline
					rows={8}
					fullWidth
					value={state.special_query}
					onChange={(e) => setState((prev) => ({ ...prev, special_query: e.target.value }))}
				/>
				<br />
				<Button
					onClick={handleAddSpecialQuery}
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
		</>
	);
}
