import getCookie from "../utils/GetCookie";
import axios from "axios";
import { useMutation } from "react-query";

async function postFormData({ path, formData }: { path: string; formData: any }) {
	const csrftoken = getCookie("csrftoken");
	return await axios.post(`/api/${path}/`, formData, {
		headers: {
			"X-CSRFToken": csrftoken,
			"Content-Type": "multipart/form-data",
		},
	});
}

export default function usePostData() {
	return useMutation(postFormData);
}
