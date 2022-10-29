import { green } from "@mui/material/colors";
import React, { useState } from "react";
import Userfront from "@userfront/react";
import { Navigate } from "react-router-dom";
import Box from "@mui/material";
import CircularProgress from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import {
	FormControl,
	Input,
	InputLabel,
	Button,
	FormHelperText,
	Autocomplete,
	TextField,
	Box,
	CircularProgress,
} from "@mui/material";
import usePostData from "../hooks/general";

export default function CreateTable() {
	if (!Userfront.accessToken()) {
		return <Navigate to='/login' />;
	} else if (Userfront.user.data && !Userfront.user.data.access === "admin") {
		return <Navigate to='/upload' />;
	}
	const { mutate: postFormData, isSuccess, error } = usePostData();
	const [inputTable, setInputTable] = useState(null);
	const [selectedFile, setSelectedFile] = useState(null);
	const [skiprows, setSkiprows] = useState(null);
	const [loading, setLoading] = useState(false);

	const onFileUpload = () => {
		setLoading(true);
		postFormData({
			path: "uploadmodel",
			formData: {
				table: inputTable,
				file: selectedFile,
				user_id: Userfront.user.userId,
				is_new_table: true,
				upload_timestamp: new Date(),
				status: "ready",
				mode: "Kézi",
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
			<Box sx={{ m: 1, position: "relative" }}>
				<Button
					variant='contained'
					endIcon={<AddIcon />}
					disabled={!inputTable || !selectedFile || loading}
					onClick={onFileUpload}>
					Létrehozás
				</Button>
				{loading && (
					<CircularProgress
						size={24}
						sx={{
							color: green[500],
							position: "absolute",
							top: "50%",
							left: "50%",
							marginTop: "-12px",
							marginLeft: "-12px",
						}}
					/>
				)}
			</Box>
			{isSuccess && <Navigate to='/upload' replace={true} />}
		</div>
	);
}
