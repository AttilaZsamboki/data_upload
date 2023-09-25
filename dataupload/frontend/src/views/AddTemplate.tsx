import React, { useState } from "react";
import { Navigate } from "react-router-dom";
import { FormControl, Input, InputLabel } from "@mui/material";
import KeyboardArrowUpIcon from "@mui/icons-material/KeyboardArrowUp";
import Button from "@mui/material/Button";
import Userfront from "@userfront/react";
import { Autocomplete, TextField } from "@mui/material";
import { useColumnNames } from "../hooks/Templates";
import usePostData from "../hooks/general";
import { useTableOptionsAll } from "../hooks/Tables";

export default function AddTemplate() {
	if (!Userfront.accessToken()) return <Navigate to='/login' replace={true} />;
	const appendOptions = ["Hozzáfűzés duplikációk szűrésével", "Hozzáfűzés", "Felülírás", "Újak frissítése"];
	const tableOptions = useTableOptionsAll();
	const [state, setState] = useState<{ table: string; pkey_col: string; skiprows: number; append: string }>({});
	const [sourceColumns, setSourceColumns] = useState({});
	const columnNames = useColumnNames(state.table);
	const { mutate: postFormData, isSuccess } = usePostData();
	const handleChange = ({ target }: { target: { name: string; value: string } }) => {
		const { name, value } = target;
		setState((values) => ({ ...values, [name]: value }));
	};

	const handleAddTemplate = () => {
		postFormData({
			path: "templates",
			formData: {
				table: state.table,
				pkey_col: state.pkey_col,
				skiprows: state.skiprows,
				append: state.append,
				source_column_names: JSON.stringify(sourceColumns),
			},
		});
	};
	React.useEffect(() => {
		document.title = "Template Hozzáadása";
	}, []);

	return (
		<div className='center-form all-white-bg p-5'>
			<h1 className='bg-slate-200 pb-6'>Template Hozzáadása</h1>
			<Autocomplete
				disablePortal
				id='table'
				options={tableOptions.data ? tableOptions.data.map((table) => table.db_table) : []}
				sx={{ width: 300 }}
				renderInput={(params) => <TextField {...params} label='Tábla neve' />}
				onChange={(e, v) => setState((prev) => ({ ...prev, table: v ? v : "" }))}
			/>
			<br />
			<TextField
				type='number'
				name='skiprows'
				label='Kihagyott sorok száma'
				value={state.skiprows}
				onChange={handleChange}
			/>
			<br />
			<Autocomplete
				disablePortal
				id='primary-key'
				options={columnNames.data?.map((column) => column)}
				sx={{ width: 300 }}
				renderInput={(params) => <TextField {...params} label='Elsődleges kulcs' />}
				onChange={(e, v) => setState((prev) => ({ ...prev, pkey_col: v }))}
				disabled={!columnNames.data || state.append !== "Hozzáfűzés duplikációk szűrésével"}
			/>
			<br />
			<Autocomplete
				disablePortal
				id='appendOptions'
				options={appendOptions}
				sx={{ width: 300 }}
				renderInput={(params) => <TextField {...params} label='Hozááfűzés formája' />}
				onChange={(e, v) => setState((prev) => ({ ...prev, append: v ? v : "" }))}
				value={state.append}
			/>
			<br />
			{columnNames.data && (
				<div>
					{columnNames.data?.map((column: string) => (
						<FormControl>
							<InputLabel htmlFor={column}>{column}</InputLabel>
							<Input
								id={column}
								name={column}
								type='text'
								onChange={({ target }) =>
									setSourceColumns((prev) => ({
										...prev,
										[target.name]: target.value,
									}))
								}
							/>
						</FormControl>
					))}
				</div>
			)}
			<Button
				onClick={handleAddTemplate}
				disabled={!columnNames}
				variant='contained'
				sx={{
					"backgroundColor": "#057D55",
					"&:hover": { color: "white" },
					"marginTop": 3,
				}}
				endIcon={<KeyboardArrowUpIcon />}
				type='submit'>
				Submit
			</Button>
			{isSuccess && <Navigate to='/upload' replace={true} />}
		</div>
	);
}
