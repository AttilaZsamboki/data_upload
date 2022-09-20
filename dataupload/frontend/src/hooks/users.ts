import { useQuery } from "react-query";
import axios from "axios";
import Userfront from "@userfront/react";

async function fetchUsersData() {
	if (["dark-frost-2k269", "winter-salad-brlnr", "ancient-river-26kn4"].includes(Userfront.user.username)) {
		const response = await axios("https://api.userfront.com/v0/users/find", {
			method: "POST",
			headers: {
				"Accept": "*/*",
				"Content-Type": "application/json",
				"Authorization": "Bearer uf_live_admin_6nz455rn_9174142975ec131dcc59fa0b55977be2",
			},
		});
		return response.data;
	}
}

async function fetchUserData() {
	const response = await axios.get("https://www.dataupload.xyz/api/users/");
	return response.data.filter((user) => user.user_id === Userfront.user.userId);
}

export function useUsersData() {
	return useQuery(["usersData"], () => fetchUsersData());
}

export function useUserData() {
	return useQuery(["userData"], () => fetchUserData());
}
