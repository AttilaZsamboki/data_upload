import axios from "axios";
import { useQuery } from "react-query";
import Userfront from "@userfront/react";

async function fetchTable(table: string) {
	if (!table) return;
	const formattedTable = table.replace(" ", "-").toLowerCase();
	const response = await axios.get(`/api/${formattedTable}`);
	return response.data;
}

async function fetchTableNames(): Promise<string[]> {
	const tablePrefix = Userfront.user.name.slice(0, 3) + "_";
	const response = await axios.get("/api/table-names");
	return response.data.filter((table: string) => table.slice(0, 4).toLowerCase() === tablePrefix.toLowerCase());
}

export function useTableOptions() {
	return useQuery(["tables"], () => fetchTableNames());
}

export function useTable(table: string) {
	return useQuery(["tables", table], () => fetchTable(table));
}