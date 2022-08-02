import React, { useState } from "react";
import { FormControl, FormHelperText, Input, InputLabel } from "@mui/material";
import LinkIcon from "@mui/icons-material/Link";
import Button from "@mui/material/Button";
import Userfront from "@userfront/react";
import getCookie from "../utils/GetCookie";

export default function AddConnection() {
	const csrftoken = getCookie("csrftoken");
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
				Accept: "application/json",
				"X-CSRFToken": csrftoken,
				"Content-Type": "application/json",
			},
			body: JSON.stringify({
				name: inputs.name,
				host: inputs.host,
				database: inputs.database,
				username: inputs.username,
				password: inputs.password,
				port: inputs.port,
				created_by: Userfront.user.userId,
			}),
		};
		fetch("/api/database-connections/", requestOptions)
			.then((response) => response.json)
			.then((data) => console.log(data))
			.catch((error) => console.log(error));
		setInputs({
			name: "",
			host: "",
			port: "",
			password: "",
			database: "",
			username: "",
		});
	};

	const formControlStyle = {
		marginBottom: 20,
		width: 500,
	};

	return (
		<form onSubmit={handleSubmit}>
			<FormControl style={formControlStyle}>
				<InputLabel htmlFor='name'>Connection Name</InputLabel>
				<Input
					id='name'
					name='name'
					type='text'
					value={inputs.name}
					onChange={handleChange}
				/>
				<FormHelperText id='name-helper'>
					You can choose any name for your connection.
				</FormHelperText>
			</FormControl>
			<br />
			<FormControl style={formControlStyle}>
				<InputLabel htmlFor='host'>Host</InputLabel>
				<Input
					id='host'
					name='host'
					type='text'
					value={inputs.host}
					onChange={handleChange}
				/>
			</FormControl>
			<br />
			<FormControl style={formControlStyle}>
				<InputLabel htmlFor='port'>Port</InputLabel>
				<Input
					id='port'
					name='port'
					type='text'
					value={inputs.port}
					onChange={handleChange}
				/>
			</FormControl>
			<br />
			<FormControl style={formControlStyle}>
				<InputLabel htmlFor='password'>Password</InputLabel>
				<Input
					id='password'
					name='password'
					type='password'
					value={inputs.password}
					onChange={handleChange}
				/>
			</FormControl>
			<br />
			<FormControl style={formControlStyle}>
				<InputLabel htmlFor='database'>Database</InputLabel>
				<Input
					id='database'
					name='database'
					type='text'
					value={inputs.database}
					onChange={handleChange}
				/>
			</FormControl>
			<br />
			<FormControl style={formControlStyle}>
				<InputLabel htmlFor='username'>Username</InputLabel>
				<Input
					id='username'
					name='username'
					type='text'
					value={inputs.username}
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
				endIcon={<LinkIcon />}
				type='submit'>
				Connect
			</Button>
		</form>
	);
}
