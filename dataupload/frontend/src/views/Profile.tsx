import * as React from "react";
import Userfront from "@userfront/react";
import Button from "@mui/material/Button";
import CloseIcon from "@mui/icons-material/Close";
import SendIcon from "@mui/icons-material/Send";
import Stack from "@mui/material/Stack";
import axios from "axios";
import getCookie from "../utils/GetCookie";
import EditIcon from "@mui/icons-material/Edit";
import TextField from "@mui/material/TextField";
import DoneIcon from "@mui/icons-material/Done";

export default function Profile() {
	const [isShown, setIsShown] = React.useState(false);
	const [isHover, setIsHover] = React.useState(false);
	const [isEditName, setIsEditName] = React.useState(false);
	const [image, setImage] = React.useState<File | undefined>();
	const [newName, setNewName] = React.useState<string | undefined>();
	const csrftoken = getCookie("csrftoken");
	const [name, setName] = React.useState(Userfront.user.name);

	const uploadProfile = async () => {
		if (typeof image == "undefined") return;
		const response = await axios.post(
			"/api/upload-profile-image/",
			{ newImage: image, oldImage: Userfront.user.image || Userfront.user.data.profileImage },
			{
				headers: {
					"X-CSRFToken": csrftoken,
					"Content-Type": "multipart/form-data",
				},
			}
		);
		await Userfront.user.update({
			data: { profileImage: `../../static/images/${image.name}` },
			image: "",
		});
		location.reload();
	};

	const changeName = async () => {
		setName(newName || name);
		setIsEditName(false);
		await Userfront.user.update({
			name: newName,
		});
	};

	return (
		<div>
			<div>
				<h1 className='text-center pb-6'>Profil</h1>
				<div className='flex flex-col items-center justify-center'>
					{isHover && (
						<EditIcon
							fontSize='small'
							onClick={() => setIsShown(true)}
							onMouseLeave={() => setIsHover(false)}
							onMouseEnter={() => setIsHover(true)}
							style={{ position: "fixed", top: 260, zIndex: 1 }}
						/>
					)}
					<img
						style={{
							width: 60,
							height: 60,
							filter: `brightness(${isHover ? 50 : 100}%)`,
							borderRadius: 9999999999,
							marginBottom: 30,
						}}
						src={Userfront.user.image || Userfront.user.data.profileImage}
						onClick={() => setIsShown(true)}
						onMouseEnter={() => setIsHover(true)}
						onMouseLeave={() => setIsHover(false)}
					/>
					<div className='flex'>
						<p className='text-lg mr-2'>
							<b style={{ marginRight: 8 }}>Név:</b>
							{!isEditName ? (
								name
							) : (
								<TextField
									onChange={(e) => setNewName(e.target.value)}
									variant='standard'
									size='small'
								/>
							)}
						</p>
						{!isEditName ? (
							<EditIcon
								style={{ marginLeft: 10, cursor: "pointer" }}
								fontSize='small'
								onClick={() => setIsEditName(true)}
							/>
						) : (
							<DoneIcon style={{ cursor: "pointer" }} fontSize='small' onClick={changeName} />
						)}
					</div>
					<div>
						<p className='text-lg'>
							<b style={{ marginRight: 8 }}>Email:</b>
							{Userfront.user.email}
						</p>
					</div>
				</div>
			</div>
			{isShown && (
				<div
					style={{
						position: "fixed",
						top: 0,
						left: 0,
						right: 0,
						bottom: 0,
						backgroundColor: "rgba(0,0,0,0.6)",
					}}>
					<div
						style={{
							position: "fixed",
							left: "20%",
							right: "20%",
							bottom: "20%",
							top: "20%",
							backgroundColor: "white",
							border: "solid 2px gray",
						}}
						className='center-form px-5'>
						<input
							className='form-control	mb-4 block w-full px-3 py-1.5 text-base font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none'
							type='file'
							id='formFile'
							onChange={(e) => setImage(e.target.files[0])}
						/>
						<Stack direction='row' spacing={2}>
							<Button
								variant='contained'
								endIcon={<SendIcon />}
								disabled={!image}
								onClick={uploadProfile}>
								Csere
							</Button>
							<Button variant='outlined' onClick={() => setIsShown(false)} startIcon={<CloseIcon />}>
								Mégsem
							</Button>
						</Stack>
					</div>
				</div>
			)}
		</div>
	);
}
