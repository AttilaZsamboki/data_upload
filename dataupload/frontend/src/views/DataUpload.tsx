import React, { useState, useRef } from "react";
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
	extension_format: "xlsx" | "csc" | "tsv";
	source_column_names: string;
};

export default function DataUpload() {
	if (!Userfront.accessToken()) return <Navigate to='/login' />;
	const inputRef = useRef(null);
	const [inputTable, setInputTable] = useState<string>();
	const [inputFile, setinputFile] = useState<File>();
	const tableOptions = useTableOptions();
	const { mutate: postFormData, isSuccess } = usePostData();

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
		<div>
			<form onSubmit={onFileUpload}>
				<Autocomplete
					disablePortal
					id='table'
					name='table'
					type='text'
					options={tableOptions.data}
					sx={{ width: 300 }}
					renderInput={(params) => <TextField {...params} label='Tábla neve' />}
					onChange={(evenet, values) => typeof values === "string" && setInputTable(values)}
					value={inputTable && inputTable.replace((Userfront.user.name.slice(0, 3) + "_").toLowerCase(), "")}
					renderOption={(props, option) => (
						<Box component='li' sx={{ "& > img": { mr: 2, flexShrink: 0 } }} {...props}>
							{option.replace((Userfront.user.name.slice(0, 3) + "_").toLowerCase(), "")}
						</Box>
					)}
				/>
				<br />
				<FormControl>
					<input
						id='file'
						name='file'
						type='file'
						onChange={(e) => setinputFile(e.target.files[0])}
						ref={inputRef}
					/>
				</FormControl>
				<br />
				<Button
					variant='contained'
					sx={{
						"backgroundColor": "#057D55",
						"&:hover": { color: "white" },
					}}
					endIcon={<FileUploadIcon />}
					type='submit'>
					Upload
				</Button>
				{isSuccess && <Navigate to='/upload' replace={true} />}
			</form>
		</div>
	);
}
