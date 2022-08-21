import React, { useState, useEffect, useRef } from "react";
import Userfront from "@userfront/react";
import { Navigate } from "react-router-dom";
import AddIcon from "@mui/icons-material/Add";
import { FormControl, Input, InputLabel, Button, FormHelperText, Autocomplete, TextField } from "@mui/material";
import usePostData from "../hooks/general";

export default function CreateTable() {
	if (!Userfront.accessToken()) {
		return <Navigate to='/login' />;
	} else if (!["dark-frost-2k269", "winter-salad-brlnr", "ancient-river-26kn4"].includes(Userfront.user.username)) {
		return <Navigate to='/upload' />;
	}

	const { mutate: postFormData, isSuccess, error } = usePostData();
	const formatOptions = ["xlsx", "csv", "tsv"];
	const [inputTable, setInputTable] = useState(null);
	const [selectedFile, setSelectedFile] = useState(null);
	const [format, setFormat] = useState(null);
	const [skiprows, setSkiprows] = useState(null);

	const onFileUpload = () => {
		postFormData({
			path: "uploadmodel",
			formData: {
				table: inputTable,
				file: selectedFile,
				user_id: Userfront.user.userId,
				is_new_table: true,
				extension_format: format,
				skiprows: skiprows,
			},
		});
	};

	return (
		<div>
			<FormControl>
				<InputLabel htmlFor='table'>Tábla neve</InputLabel>
				<Input
					id='table'
					name='table'
					type='text'
					value={inputTable}
					onChange={({ target }) => setInputTable(target.value)}
				/>
			</FormControl>
			<br />
			<Autocomplete
				disablePortal
				id='format'
				options={formatOptions}
				sx={{ width: 300 }}
				renderInput={(params) => <TextField {...params} label='Fájlformátum' />}
				onChange={(event, values) => setFormat(values)}
			/>
			<br />
			<TextField
				type='number'
				name='skiprows'
				label='Kihagyott sorok száma'
				value={skiprows}
				onChange={({ target }) => setSkiprows(target.value)}
			/>
			<br />
			<FormControl>
				<input id='file' name='file' type='file' onChange={({ target }) => setSelectedFile(target.files[0])} />
				<FormHelperText>Példa File</FormHelperText>
			</FormControl>
			<br />
			<Button
				onClick={onFileUpload}
				variant='contained'
				sx={{
					"backgroundColor": "#057D55",
					"&:hover": { color: "white" },
				}}
				endIcon={<AddIcon />}
				type='submit'>
				Létrehozás
			</Button>
			{isSuccess && <Navigate to='/upload' replace={true} />}
		</div>
	);
}
