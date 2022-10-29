import React, { useState } from "react";
import { Navigate } from "react-router-dom";
import { FormControl, Input, InputLabel } from "@mui/material";
import KeyboardArrowUpIcon from "@mui/icons-material/KeyboardArrowUp";
import Button from "@mui/material/Button";
import Userfront from "@userfront/react";
import { Autocomplete, TextField } from "@mui/material";
import usePostData from "../hooks/general";
import { useQuery } from "react-query";
import axios from "axios";
import { useUserGroups } from "../hooks/users";

export default function AddTemplate() {
	if (!Userfront.accessToken()) return <Navigate to='/login' replace={true} />;
	const [state, setState] = useState<{
		db_table: string;
		verbose_name: string;
		available_at: string;
		group: string;
	}>();
	const userGroups = useUserGroups();
	const tableOverview = useQuery(["tablenames"], async () => {
		return await axios.get("/api/table-names");
	});
	const { mutate: postFormData, isSuccess } = usePostData();
	const handleAddTemplate = () => {
		if (!state) return;
		postFormData({
			path: "table-overview",
			formData: {
				db_table: state.db_table,
				verbose_name: state.verbose_name,
				available_at: state.available_at.toString(),
				email_name: state.email_name,
				group: state.group,
			},
		});
	};
	return (
		<div className='center-form all-white-bg p-5'>
			<h1 className='bg-slate-200 pb-6'>Tábla Áttekintés Hozzáadása</h1>
			<Autocomplete
				disablePortal
				id='available-at'
				options={tableOverview.data?.data}
				sx={{ width: 300 }}
				renderInput={(params) => <TextField {...params} label='Tábla' />}
				onChange={(e, v) => setState((prev) => ({ ...prev, db_table: v }))}
			/>
			<br />
			<Autocomplete
				disablePortal
				id='group'
				options={userGroups.data?.map((group) => group.group)}
				sx={{ width: 300 }}
				renderInput={(params) => <TextField {...params} label='Csoport' />}
				onChange={(e, v) => setState((prev) => ({ ...prev, group: v }))}
			/>
			<br />
			<FormControl>
				<InputLabel htmlFor='verbose-name'>Felületen látható név</InputLabel>
				<Input
					id='verbose-name'
					name='verbose-name'
					type='text'
					sx={{ width: 300, height: 30 }}
					onChange={({ target }) => setState((prev) => ({ ...prev, verbose_name: target.value }))}
				/>
			</FormControl>
			<br />
			<Autocomplete
				multiple
				disablePortal
				id='available-at'
				options={["grid", "upload"]}
				sx={{ width: 300 }}
				renderInput={(params) => <TextField {...params} label='Elérhetőség' />}
				onChange={(e, v) => setState((prev) => ({ ...prev, available_at: v }))}
			/>
			<br />
			{state?.available_at.includes("upload") && (
				<FormControl>
					<InputLabel htmlFor='email-name'>Email név</InputLabel>
					<Input
						id='email-name'
						name='email-name'
						type='text'
						sx={{ width: 300, height: 30 }}
						onChange={({ target }) => setState((prev) => ({ ...prev, email_name: target.value }))}
					/>
				</FormControl>
			)}
			<Button
				onClick={handleAddTemplate}
				disabled={!state}
				variant='contained'
				sx={{
					"backgroundColor": "#057D55",
					"&:hover": { color: "white" },
					"marginTop": 3,
				}}
				endIcon={<KeyboardArrowUpIcon />}
				type='submit'>
				Hozzáadás
			</Button>
			{isSuccess && <Navigate to='/upload' replace={true} />}
		</div>
	);
}
