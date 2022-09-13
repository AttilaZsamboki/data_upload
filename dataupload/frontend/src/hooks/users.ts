import { useQuery } from "react-query";
import axios from "axios";
import Userfront from "@userfront/react";

async function fetchUserData() {
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

export function useUserData() {
	return useQuery(["userData"], () => fetchUserData());
}
