import axios from "axios";
import { useQuery } from "react-query";
import getCookie from "../utils/GetCookie";

type TemplateData = {
	table: string;
	pkey_col: string;
	skiprows: number;
	append: string;
	source_column_names: string;
};

export async function fetchColumnNames(table: string, dtype: boolean) {
	const response = await axios.get("/api/column-names");
	const filteredData = response.data
		.filter((column: string[]) => column[0] === table)
		.map((column: string[]) => (!dtype ? column[1] : [column[1], column[2]]));
	return filteredData;
}

export function useColumnNames(table: string | undefined) {
	return useQuery(["column-names", table], () => {
		if (typeof table === "string") {
			return fetchColumnNames(table, false);
		}
	});
}

export function useColumnDtypes(table: string | undefined) {
	return useQuery(["column-names", table], () => {
		if (typeof table === "string") {
			return fetchColumnNames(table, true);
		}
	});
}

function addTemplate(formData: TemplateData) {
	const csrftoken = getCookie("csrftoken");
	axios
		.post("/api/templates/", formData, {
			headers: {
				"X-CSRFToken": csrftoken,
				"Content-Type": "multipart/form-data",
			},
		})
		.then((res) => res.data);
}
