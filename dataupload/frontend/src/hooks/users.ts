import { useQuery } from "react-query";
import axios from "axios";
import Userfront from "@userfront/react";

interface UserGroups {
	group: string;
	tables: string[];
	user_ids: number[];
}

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

async function fetchUserTables(groupName: string | undefined) {
	let response = await axios.get("/api/groups");
	response = response.data;
	if (typeof groupName === "undefined") {
		return response.find((group: UserGroups) => group.group === Userfront.user.data.group[0]);
	}
	return response.find((group: UserGroups) => group.group === groupName);
}

async function fetchUserGroups(): Promise<UserGroups[]> {
	const response = await axios.get("/api/groups");
	return response.data;
}

export function useUserGroups() {
	return useQuery(["userGroups"], () => fetchUserGroups());
}

export function useUsersData() {
	return useQuery(["usersData"], () => fetchUsersData());
}

export function useGroupTables(groupName: string | undefined) {
	return useQuery(["group", groupName], () => fetchUserTables(groupName));
}
