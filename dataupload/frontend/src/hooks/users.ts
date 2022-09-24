import { useQuery } from "react-query";
import axios from "axios";
import Userfront from "@userfront/react";

async function fetchUsersData() {
	if (Userfront.user.data && Userfront.user.data.access === "admin") {
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

async function fetchUserTables() {
	const response = await axios.get("/api/groups");
	return response.data.find((group: { group: string; table: string[] }) => group.group === Userfront.user.data.group)
		.tables;
}

export function useUsersData() {
	return useQuery(["usersData"], () => fetchUsersData());
}

export function useGroupTables() {
	return useQuery(["group"], () => fetchUserTables());
}
