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
		<div className='center-form mx-80 py-20 my-32'>
			<div className='flex justify-center'>
				<div className='mb-3 w-96 object-left-top'>
					<label htmlFor='formFile'>Válassz ki egy fájlt:</label>
					<input
						className='form-control	block w-full px-3 py-1.5 text-base font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none'
						type='file'
						id='formFile'
						onChange={(e) => setSelectedFile(e.target.files[0])}
					/>
				</div>
			</div>
			<br />
			<Autocomplete
				className='bg-white'
				disablePortal
				id='format'
				options={formatOptions}
				sx={{ width: 300 }}
				renderInput={(params) => <TextField {...params} label='Fájlformátum' />}
				onChange={(event, values) => setFormat(values)}
			/>
			<br />
			<FormControl>
				<InputLabel htmlFor='table'>Tábla neve</InputLabel>
				<Input
					className='better-base-input bg-white'
					sx={{ height: 50 }}
					id='table'
					name='table'
					type='text'
					value={inputTable}
					onChange={({ target }) => setInputTable(target.value)}
				/>
			</FormControl>
			<br />
			<TextField
				type='number'
				className='bg-white'
				name='skiprows'
				label='Kihagyott sorok száma'
				value={skiprows}
				onChange={({ target }) => setSkiprows(target.value)}
			/>
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
