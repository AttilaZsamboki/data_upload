import * as React from "react";
import { Button, Autocomplete, TextField } from "@mui/material";
import { Link, Navigate } from "react-router-dom";
import { useTableOptions } from "../hooks/Tables";
import { atom, useAtom } from "jotai";
import Userfront from "@userfront/react";
import usePostData from "../hooks/general";
import axios from "axios";
import CircularProgress from "@mui/material/CircularProgress";
import Box from "@mui/material/Box";
import DoneIcon from "@mui/icons-material/Done";
import ClearIcon from "@mui/icons-material/Clear";
import getCookie from "../utils/GetCookie";

const csrftoken = getCookie("csrftoken");
const idAtom = atom(null);

export function DataUploadStart() {
	return (
		<>
			{window.localStorage.getItem("upload_id") !== "" ? (
				<Navigate to='/upload-checker' replace={true} />
			) : (
				<div className='flex flex-col items-center justify-center'>
					<h1>Feltöltés</h1>
					<Link to='/upload'>
						<Button sx={{ "marginTop": 5, "&:hover": { color: "white" } }} variant='contained'>
							Kezdés
						</Button>
					</Link>
				</div>
			)}
		</>
	);
}

export function DataUploadInput() {
	const { data, mutate: postFormData, isSuccess } = usePostData();
	const [selectedFile, setSelectedFile] = React.useState<any>(null);
	const [isButton, setIsButton] = React.useState(false);
	const tableOptionsRaw = useTableOptions();
	const tableOptions =
		typeof tableOptionsRaw.data !== "undefined" && tableOptionsRaw.data.map((table) => table.slice(4));
	const [selectedTable, setSelectedTable] = React.useState<string | null>(null);
	const [uploadId, setUploadId] = useAtom(idAtom);
	React.useEffect(() => {
		if (selectedFile && tableOptions) {
			setSelectedTable("");
			let foundTable = false;
			tableOptions.forEach((table) => {
				if (selectedFile.name.includes(table)) {
					setSelectedTable(table);
					foundTable = true;
				}
			});
			foundTable ? setIsButton(false) : setIsButton(true);
		}
	}, [selectedFile]);
	const startChecker = (e: any) => {
		const tablePrefix = Userfront.user.name.slice(0, 3) + "_";
		e.preventDefault();
		postFormData({
			path: "uploadmodel",
			formData: {
				file: selectedFile,
				table: tablePrefix.toLowerCase() + selectedTable,
				user_id: Userfront.user.userId,
				status: "waiting for processing",
				timestamp: new Date(),
			},
		});
	};
	setUploadId(data?.data.id);
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
				{isButton && (
					<Autocomplete
						sx={{ backgroundColor: "white" }}
						options={tableOptions}
						renderInput={(params) => <TextField {...params} label='Tábla neve' />}
						onChange={(e, v) => setSelectedTable(v)}
					/>
				)}
			</div>
			<Button variant='contained' disabled={!selectedTable || !selectedFile} onClick={startChecker}>
				Tovább
			</Button>
			{isSuccess && <Navigate to='/upload-checker' replace={true} />}
		</div>
	);
}

interface ExtStatus {
	overall_status: boolean;
	gotten: string;
	expected: string[];
}

interface ColStatus {
	overall_status: boolean | "";
	missing_cols: string;
	wrong_cols: string;
	gotten: string;
	expected: string[];
}

interface ConentStatus {
	overall_status: boolean | "";
	error: [
		{
			error_col: string;
			error: string;
		}
	];
}

export function DataUploadChecker() {
	const [uploadId, setUploadId] = useAtom(idAtom);
	const [IsDeleted, setIsDeleted] = React.useState(false);
	const [isSuccess, setIsSuccess] = React.useState(false);
	const [extensionFormatStatus, setExtensionFormatStatus] = React.useState<ExtStatus | "Loading">("Loading");
	const [columnNamesStatus, setColumnNamesStatus] = React.useState<ColStatus | "Loading">("Loading");
	const [columnConentStatus, setColumnContentStatus] = React.useState<ConentStatus | "Loading">("Loading");
	const wsRef = React.useRef<any>();
	React.useEffect(() => {
		uploadId && window.localStorage.setItem("upload_id", uploadId), [uploadId];
	});
	React.useEffect(() => {
		setUploadId(window.localStorage.getItem("upload_id")), [];
	});
	React.useEffect(() => {
		if (uploadId) {
			const uploadSocket = new WebSocket(`wss://${window.location.host}/ws/upload/${uploadId}/`);
			wsRef.current = uploadSocket;
			uploadSocket.onmessage = function (e) {
				const data = JSON.parse(e.data);
				setExtensionFormatStatus(data.extension_format);
				setColumnNamesStatus(data.column_names);
				setColumnContentStatus(data.column_content);
			};
			uploadSocket.onclose = (e) => {
				console.error("Upload socket cloesed unexpectedly");
			};
			return () => {
				uploadSocket.close();
			};
		}
	}, [uploadId]);
	const deleteUpload = async () => {
		await axios.delete(`/api/uploadmodel/${uploadId}/`, {
			headers: {
				"X-CSRFToken": csrftoken,
				"Content-Type": "multipart/form-data",
			},
		});
		window.localStorage.setItem("upload_id", "");
		!window.localStorage.getItem("upload_id") && setIsDeleted(true);
		setUploadId("");
	};
	const startUpload = (e: any) => {
		e.preventDefault();
		wsRef.current.send(JSON.stringify({ upload: true }));
		window.localStorage.setItem("upload_id", "");
		!window.localStorage.getItem("upload_id") && setIsSuccess(true);
		setUploadId("");
	};
	return (
		<div>
			<div className='upload-checker-container'>
				<h2 className='font-medium text-lg'>Fájlformátum:</h2>
				{extensionFormatStatus === "Loading" ? (
					<Box>
						<CircularProgress />
					</Box>
				) : extensionFormatStatus?.overall_status ? (
					<DoneIcon color='success' fontSize='large' />
				) : (
					<>
						<ClearIcon sx={{ color: "red" }} fontSize='large' />
						<div className='border border-gray-300 rounded-lg p-4'>
							<br />
							<span className='font-medium mr-3'>Kapott formátum:</span>
							<p>{extensionFormatStatus?.gotten},</p>
							<br />
							<span className='font-medium mr-3'>Elfogadott formátumok: </span>
							<p>{extensionFormatStatus?.expected}</p>
						</div>
					</>
				)}
			</div>
			{columnNamesStatus !== "Loading" && columnNamesStatus?.overall_status !== "" && (
				<div className='upload-checker-container'>
					<h2 className='font-medium text-lg whitespace-nowrap'>Oszlop nevek:</h2>
					{columnNamesStatus?.missing_cols ? (
						<ClearIcon sx={{ color: "red", marginLeft: 10 }} fontSize='large' />
					) : columnNamesStatus?.wrong_cols ? (
						<ClearIcon sx={{ color: "#DEC20B", marginLeft: 10 }} fontSize='large' />
					) : (
						<DoneIcon color='success' fontSize='large' />
					)}
					<div className='border border-gray-300 rounded-lg p-4 ml-24'>
						<span className='font-medium mr-3'>Hiányzó oszlopok: </span>
						{columnNamesStatus?.missing_cols ? (
							<p>{columnNamesStatus?.missing_cols}</p>
						) : (
							<DoneIcon color='success' />
						)}
						<br />
						<span className='font-medium mr-3'>Nem létező oszlopok: </span>
						{columnNamesStatus?.wrong_cols ? (
							<p>
								{columnNamesStatus?.wrong_cols},<br />
							</p>
						) : (
							<DoneIcon color='success' />
						)}
						{(columnNamesStatus?.missing_cols || columnNamesStatus?.wrong_cols) && (
							<>
								<span className='font-medium mr-3'>Kapott oszlopok: </span>
								<br />
								<p>{columnNamesStatus.gotten}</p>
							</>
						)}
					</div>
				</div>
			)}
			{columnConentStatus !== "Loading" && columnConentStatus.overall_status !== "" && (
				<div className='upload-checker-container'>
					<h2 className='font-medium text-lg'>Oszlop tartalmi állapota:</h2>
					{columnConentStatus === "Loading" ? (
						<Box sx={{ display: "flex" }}>
							<CircularProgress />
						</Box>
					) : columnConentStatus?.error.length ? (
						<>
							<ClearIcon sx={{ color: "red " }} fontSize='large' />
							<div>
								{columnConentStatus.error.map((error) => (
									<div className='border border-gray-300 rounded-lg p-4 mb-4'>
										{error.error.split(":")[0] === "could not convert string to float" ? (
											<>
												<span className='font-medium mr-3'>
													{
														error.error
															.replace(
																"could not convert string to float:",
																"Nem tudta a stringet floattá alakítani:"
															)
															.split(":")[0]
													}
													:
												</span>
												<p>{error.error.split(":")[1]}</p>
											</>
										) : error.error.split(":")[0] === "Unknown string format" ? (
											<>
												<span className='font-medium mr-3'>
													{
														error.error
															.replace(
																"Unknown string format:",
																"Ismeretlen string formátum:"
															)
															.split(":")[0]
													}
													:
												</span>
												<p>{error.error.split(":")[1]}</p>
											</>
										) : (
											error.error
										)}
										<br />
										<span className='font-medium mr-3'>Oszlop:</span> <p>{error.error_col}</p>
									</div>
								))}
							</div>
						</>
					) : (
						<DoneIcon color='success' fontSize='large' />
					)}
				</div>
			)}
			<div className='container mx-auto px-4'>
				<Button variant='outlined' color='error' onClick={deleteUpload} sx={{ margin: 10 }}>
					Feltöltés törlése
				</Button>
				<Button
					variant='contained'
					disabled={
						extensionFormatStatus === "Loading" ||
						!extensionFormatStatus.overall_status ||
						columnNamesStatus === "Loading" ||
						!columnNamesStatus.overall_status ||
						columnConentStatus === "Loading" ||
						!columnConentStatus.overall_status
					}
					onClick={startUpload}>
					Feltöltés!
				</Button>
				{IsDeleted && <Navigate to='/upload-start' replace={true} />}
				{isSuccess && <Navigate to='/uploads' replace={true} />}
			</div>
		</div>
	);
}
