import axios from "axios";
import { useQuery, useMutation } from "react-query";
import getCookie from "../utils/GetCookie";

export async function fetchColumnNames(table) {
	if (!table) return;
	const response = await axios.get("/api/column-names");
	return response.data.filter((column) => column[0] === table && column[1] !== "id").map((column) => column[1]);
}

export function useColumnNames(table) {
	if (!table) return;
	return useQuery(["column-names", table], () => fetchColumnNames(table));
}

function addTemplate(formData) {
	const csrftoken = getCookie("csrftoken");
	axios({
		method: "post",
		url: "/api/templates/",
		data: formData,
		headers: {
			"X-CSRFToken": csrftoken,
			"Content-Type": "multipart/form-data",
		},
	}).then((res) => res.data);
}

export function useCreateTemplate() {
	return useMutation(addTemplate);
}
