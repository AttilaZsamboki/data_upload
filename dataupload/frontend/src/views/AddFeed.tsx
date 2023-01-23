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
import { useUsersData } from "../hooks/users";

export default function AddFeed() {
	if (!Userfront.accessToken()) return <Navigate to='/login' replace={true} />;
	const [state, setState] = useState<{ url: string; table: string; userName: number; frequency: string }>();
	const tableOverview = useQuery(["table-names"], async () => {
		return await axios.get("/api/table-names");
	});
	const { mutate: postFormData, isSuccess } = usePostData();
	const userData = useUsersData();
	const handleAddTemplate = () => {
		if (!state) return;
		postFormData({
			path: "feed",
			formData: {
				url: state.url,
				table: state.table,
				user_id: userData.data.results
					.filter((user) => user.name === state.userName)
					.map((user) => user.userId)
					.toString(),
				frequency: state.frequency,
				runs_at: state.runs_at,
			},
		});
	};
	React.useEffect(() => {
		document.title = "Feed Hozzáadása";
	}, []);
	let hours = [];
	for (let i = 0; i < 24; i++) {
		hours.push(i);
	}
	return (
		<div className='center-form all-white-bg p-5'>
			<h1 className='bg-slate-200 pb-6'>Feed Hozzáadása</h1>
			<Autocomplete
				disablePortal
				id='table'
				options={tableOverview.data?.data}
				sx={{ width: 300 }}
				renderInput={(params) => <TextField {...params} label='Tábla' />}
				onChange={(e, v) => setState((prev) => ({ ...prev, table: v }))}
			/>
			<br />
			<FormControl>
				<InputLabel htmlFor='url'>URL</InputLabel>
				<Input
					id='url'
					name='url'
					type='text'
					sx={{ width: 300, height: 30 }}
					onChange={({ target }) => setState((prev) => ({ ...prev, url: target.value }))}
				/>
			</FormControl>
			<br />
			<Autocomplete
				disablePortal
				id='userName'
				options={userData.isFetched && userData.data.results.map((user) => user.name)}
				sx={{ width: 300 }}
				renderInput={(params) => <TextField {...params} label='Felhasználó' />}
				onChange={(e, v) => setState((prev) => ({ ...prev, userName: v }))}
			/>
			<Autocomplete
				disablePortal
				id='frequency'
				options={["1 óra", "1 nap"]}
				sx={{ width: 300 }}
				renderInput={(params) => <TextField {...params} label='Frekvencia' />}
				onChange={(e, v) => setState((prev) => ({ ...prev, frequency: v }))}
			/>
			<Autocomplete
				disablePortal
				className='my-4'
				id='runs-at'
				options={hours}
				sx={{ width: 300 }}
				renderInput={(params) => <TextField {...params} label='Futás ideje' />}
				onChange={(e, v) => setState((prev) => ({ ...prev, runs_at: v }))}
			/>
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
