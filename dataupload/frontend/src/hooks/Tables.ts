import axios from "axios";
import { useQuery } from "react-query";

interface tableOptions {
	id: number;
	db_table: string;
	verbose_name: string;
	email_name: string | undefined;
	group: string;
}

async function fetchTable(table: string) {
	if (!table) return;
	const formattedTable = table.replace(" ", "-").toLowerCase();
	const response = await axios.get(`/api/${formattedTable}`);
	return response.data;
}

async function fetchTableNames(filter: boolean): Promise<tableOptions[]> {
	const response = await axios.get("/api/table-overview");
	if (filter) return response.data;
	return response.data;
}
export function useTableOptions() {
	return useQuery(["tables"], () => fetchTableNames(false));
}

export function useTableOptionsAll() {
	return useQuery(["tables-all"], () => fetchTableNames(true));
}

export function useTable(table: string) {
	return useQuery(["tables", table], () => fetchTable(table));
}
