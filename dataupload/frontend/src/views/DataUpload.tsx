import React, { useState, useRef, useEffect } from "react";
import Userfront from "@userfront/react";
import { Navigate } from "react-router-dom";
import { Autocomplete } from "@mui/material";
import FileUploadIcon from "@mui/icons-material/FileUpload";
import { FormControl, TextField, Box, Button } from "@mui/material";
import usePostData from "../hooks/general";
import { useTableOptions } from "../hooks/Tables";

type TemplateType = {
	id: number;
	table: string;
	pkey_col: string;
	skiprows: number;
	created_by_id: number;
	append: "Felülírás" | "Hozzáfűzés" | "Hozzáfűzés duplikációk szűrésével";
	source_column_names: string;
};

export default function DataUpload() {
	if (!Userfront.accessToken()) return <Navigate to='/login' />;
	const inputRef = useRef(null);
	const [inputTable, setInputTable] = useState<string>();
	const [inputFile, setInputFile] = useState<File>();
	const tableOptions = useTableOptions();
	const { mutate: postFormData, isSuccess } = usePostData();

	useEffect(() => {
		document.title = "Upload";
	}, []);

	const onFileUpload = (e) => {
		postFormData({
			path: "uploadmodel",
			formData: {
				table: inputTable,
				file: inputFile,
				user_id: Userfront.user.userId,
				is_new_table: false,
			},
		});
		if (isSuccess) {
			window.location.reload(false);
		}
	};

	return (
		<form className='center-form' onSubmit={onFileUpload}>
			<h1 className='pb-16'>Fájl Feltöltése</h1>
			<div className='flex justify-center'>
				<div className='mb-3 w-96 object-left-top'>
					<label htmlFor='formFile'>Válassz ki egy fájlt (.xlsx, .csv, .tsv):</label>
					<input
						className='form-control	block w-full px-3 py-1.5 text-base font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none'
						type='file'
						id='formFile'
						onChange={(e) => setInputFile(e.target.files[0])}
					/>
				</div>
			</div>
			<br />
			<Autocomplete
				className='bg-white col-span-1'
				disablePortal
				id='table'
				name='table'
				type='text'
				options={tableOptions.data}
				sx={{ width: 300 }}
				renderInput={(params) => <TextField {...params} label='Tábla neve' />}
				onChange={(e, values) => typeof values === "string" && setInputTable(values)}
				value={inputTable && inputTable.replace((Userfront.user.name.slice(0, 3) + "_").toLowerCase(), "")}
				renderOption={(props, option) => (
					<Box component='li' sx={{ "& > img": { mr: 2, flexShrink: 0 } }} {...props}>
						{option.replace((Userfront.user.name.slice(0, 3) + "_").toLowerCase(), "")}
					</Box>
				)}
			/>
			<br />
			<Button
				disabled={!inputFile}
				variant='contained'
				className=''
				sx={{
					"backgroundColor": "#057D55",
					"&:hover": { color: "white" },
					"marginTop": 3,
				}}
				endIcon={<FileUploadIcon />}
				type='submit'>
				Feltöltés
			</Button>
			{isSuccess && <Navigate to='/upload' replace={true} />}
		</form>
	);
}
