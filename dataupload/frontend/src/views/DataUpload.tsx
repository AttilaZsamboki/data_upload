import * as React from "react";
import { Button, Autocomplete, TextField } from "@mui/material";
import { Link } from "react-router-dom";
import { useTableOptions } from "../hooks/Tables";
import { atom, useAtom } from "jotai";

const tableAtom = atom(null);

export function DataUploadStart() {
	return (
		<div className='flex flex-col items-center justify-center'>
			<h1>Feltöltés</h1>
			<Link to='/upload'>
				<Button sx={{ "marginTop": 5, "&:hover": { color: "white" } }} variant='contained'>
					Kezdés
				</Button>
			</Link>
		</div>
	);
}

export function DataUploadInput() {
	const [selectedFile, setSelectedFile] = React.useState(null);
	const tableOptionsRaw = useTableOptions();
	const tableOptions =
		typeof tableOptionsRaw.data !== "undefined" && tableOptionsRaw.data.map((table) => table.slice(4));
	const [selectedTable, setSelectedTable] = React.useState(tableAtom);
	React.useEffect(() => {
		if (selectedFile && tableOptions) {
			tableOptions.forEach((table) => {
				if (selectedFile.name.includes(table)) {
					setSelectedTable(table);
				}
			});
		}
	}, [selectedFile]);
	return (
		<div className='center-form'>
			<div className='mb-3 w-96 object-left-top break-after-column'>
				<label htmlFor='formFile'>Válassz ki egy fájlt:</label>
				<input
					className='form-control	block w-full px-3 py-1.5 text-base font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none'
					type='file'
					id='formFile'
					onChange={(e) => setSelectedFile(e.target.files[0])}
				/>
				<br />
				{!selectedTable && !tableOptionsRaw.isLoading && selectedFile && (
					<Autocomplete
						sx={{ backgroundColor: "white" }}
						options={tableOptions}
						renderInput={(params) => (
							<TextField {...params} label='Tábla neve' onChange={(e, v) => setSelectedTable(v)} />
						)}
					/>
				)}
			</div>
			<Link to='/upload-checker'>
				<Button variant='contained'>Tovább</Button>
			</Link>
		</div>
	);
}
console.log(tableAtom);

export function DataUploadChecker() {
	const [table, setTable] = useAtom(tableAtom);
	return (
		<div>
			<h1>{table}</h1>
		</div>
	);
}
