import axios from "axios";
import { useMutation } from "react-query";
import getCookie from "../utils/GetCookie";

function addSpecialQuery(formData) {
	const csrftoken = getCookie("csrftoken");
	axios({
		method: "post",
		url: "/api/special-queries/",
		data: formData,
		headers: {
			"X-CSRFToken": csrftoken,
			"Content-Type": "multipart/form-data",
		},
	}).then((res) => res.data);
}

export default function useCreateSpecialQuery() {
	return useMutation(addSpecialQuery);
}
