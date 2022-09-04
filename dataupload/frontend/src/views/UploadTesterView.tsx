import * as React from "react";
import Button from "@mui/material/Button";
import Userfront from "@userfront/react";

export default function UploadTester() {
	const [selectedFile, setSelectedFile] = React.useState();
	const [selectedTable, setSelectedTable] = React.useState();
	const [uploadLog, setUploadLog] = React.useState();
	const chatSocket = new WebSocket(`ws://${window.location.host}/ws/upload/${Userfront.user.userId}/`);
	chatSocket.onmessage = function (e) {
		const data = JSON.parse(e.data);
		setUploadLog(data.message);
	};
	chatSocket.onclose = function (e) {
		console.error("Chat socket closed unexpectedly");
	};
	let reader = new FileReader();
	var rawData = new ArrayBuffer();
	reader.onload = function (e) {
		rawData = e.target.result;
		chatSocket.send(rawData);
	};
	const uploadSender = (e) => {
		e.preventDefault();
		reader.readAsArrayBuffer(selectedFile);
	};
	return (
		<div className='center-form'>
			<p>{uploadLog}</p>
			<div className='mb-3 w-96 object-left-top break-after-column'>
				<label htmlFor='formFile'>Válassz ki egy fájlt:</label>
				<input
					className='form-control	block w-full px-3 py-1.5 text-base font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none'
					type='file'
					id='formFile'
					onChange={(e) => setSelectedFile(e.target.files[0])}
				/>
			</div>
			<input
				className='block'
				type='text'
				name='input-upload-table'
				id='upload-table'
				onChange={(e) => setSelectedTable(e.target.value)}
			/>
			<Button sx={{ marginTop: 5 }} onClick={uploadSender} variant='contained'>
				Upload
			</Button>
		</div>
	);
}
