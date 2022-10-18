import { Autocomplete, Stack, TextField, Button } from "@mui/material";
import * as React from "react";
import { useTableOptionsAll } from "../hooks/Tables";
import { useUsersData } from "../hooks/users";
import Alert from "@mui/material/Alert";
import SendIcon from "@mui/icons-material/Send";
import axios, { AxiosResponse } from "axios";
import getCookie from "../utils/GetCookie";
import { useAutoAnimate } from "@formkit/auto-animate/react";

export default function AddGroup() {
	const { data, isLoading } = useTableOptionsAll();
	const [animationParent] = useAutoAnimate();
	const userData = useUsersData();
	const [state, setState] = React.useState<any>();
	const [isError, setIsError] = React.useState(false);
	const [errorMsg, setErrorMsg] = React.useState<string | undefined>("");
	const [errorMappings] = React.useState<[{ original: string; visual: string }]>([
		{ original: "dataupload groups with this group already exists.", visual: "Csoport már létezik" },
	]);

	const addGroup = async () => {
		setIsError(false);
		const csrftoken = getCookie("csrftoken");
		try {
			const response = await axios.post(
				"/api/groups/",
				{
					group: state.group,
					tables: state.tables.map((table) => table.db_table).toString(),
					user_ids: state.userIds.map((user) => user.userId).toString(),
				},
				{
					headers: {
						"X-CSRFToken": csrftoken,
						"Content-Type": "application/json",
					},
				}
			);
		} catch (e: AxiosResponse) {
			setIsError(true);
			setErrorMsg(errorMappings.find((error) => error.original === e.response.data.group.toString())?.visual);
			return;
		}
		window.location.replace("/import-config");
	};
	React.useEffect(() => {
		if (isError === true) {
			setInterval(() => isError && setIsError(false), 10000);
		}
	}, [isError]);
	return (
		<div ref={animationParent}>
			{isError && (
				<div className='flex flex-col justify-center items-center'>
					<Alert
						onClose={() => setIsError(false)}
						sx={{ marginTop: -16, marginBottom: -20 }}
						severity='error'>
						{errorMsg}
					</Alert>
				</div>
			)}
			<div className='center-form'>
				<h1 className='mb-4'>Csoport Hozzáadása</h1>
				<Stack spacing={3} sx={{ width: 500 }}>
					<TextField
						style={{ backgroundColor: "white", margin: 10 }}
						variant='outlined'
						label='Csoport Neve'
						onChange={(e) => setState((prev) => ({ ...prev, group: e.target.value }))}
					/>
					<Autocomplete
						style={{ backgroundColor: "white", margin: 10 }}
						multiple
						options={!isLoading && data}
						getOptionLabel={(option) => option.db_table}
						renderInput={(params) => <TextField {...params} variant='outlined' label='Táblák' />}
						onChange={(e, v) => setState((prev) => ({ ...prev, tables: v }))}
					/>
					<Autocomplete
						style={{ backgroundColor: "white", margin: 10 }}
						multiple
						options={!userData.isLoading && userData?.data?.results}
						getOptionLabel={(option) => option.userId}
						renderInput={(params) => <TextField {...params} variant='outlined' label='Felhasználók' />}
						onChange={(e, v) => setState((prev) => ({ ...prev, userIds: v }))}
					/>
				</Stack>
				<Stack direction='row' spacing={2}>
					<Button
						variant='contained'
						endIcon={<SendIcon />}
						disabled={!state?.group || !state?.tables || !state?.userIds}
						onClick={addGroup}
						sx={{ marginTop: 3 }}>
						Hozzáadás
					</Button>
				</Stack>
			</div>
		</div>
	);
}
