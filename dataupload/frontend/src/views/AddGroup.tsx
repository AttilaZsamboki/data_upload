import { Autocomplete, Stack, TextField, Button } from "@mui/material";
import * as React from "react";
import { useTableOptionsAll } from "../hooks/Tables";
import { useUsersData } from "../hooks/users";
import { Navigate } from "react-router-dom";
import SendIcon from "@mui/icons-material/Send";
import axios from "axios";
import getCookie from "../utils/GetCookie";

export default function AddGroup() {
	const { data, isLoading } = useTableOptionsAll();
	const userData = useUsersData();
	const [state, setState] = React.useState<any>();
	const addGroup = async () => {
		if (state === undefined) return;
		const csrftoken = getCookie("csrftoken");
		const response = await axios.post(
			"/api/groups/",
			{
				group: state.group,
				tables: state.tables.map((table) => table.db_table),
				user_ids: state.userIds.map((user) => user.userId),
			},
			{
				headers: {
					"X-CSRFToken": csrftoken,
					"Content-Type": "application/json",
				},
			}
		);
		window.location.replace("http://127.0.0.1:8000/import-config/");
	};
	if (isLoading) return;
	return (
		<div className='center-form'>
			<h1>Csoport Hozzáadása</h1>
			<TextField
				variant='outlined'
				label='Csoport Neve'
				onChange={(e) => setState((prev) => ({ ...prev, group: e.target.value }))}
			/>
			<Autocomplete
				multiple
				options={data}
				getOptionLabel={(option) => option.db_table}
				renderInput={(params) => <TextField {...params} variant='outlined' label='Táblák' />}
				onChange={(e, v) => setState((prev) => ({ ...prev, tables: v }))}
			/>
			<Autocomplete
				multiple
				options={userData?.data?.results}
				getOptionLabel={(option) => option.userId}
				renderInput={(params) => <TextField {...params} variant='outlined' label='Felhasználók' />}
				onChange={(e, v) => setState((prev) => ({ ...prev, userIds: v }))}
			/>
			<Stack direction='row' spacing={2}>
				<Button
					variant='contained'
					endIcon={<SendIcon />}
					disabled={!state?.group || !state?.tables || !state?.userIds}
					onClick={addGroup}>
					Hozzáadás
				</Button>
			</Stack>
		</div>
	);
}
