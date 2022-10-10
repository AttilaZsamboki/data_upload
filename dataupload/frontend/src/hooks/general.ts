import getCookie from "../utils/GetCookie";
import axios from "axios";
import { useMutation } from "react-query";

async function postFormData({
	path,
	formData,
	contentType = "multipart/form-data",
}: {
	path: string;
	formData: any;
	contentType?: string;
}) {
	const csrftoken = getCookie("csrftoken");
	return await axios.post(`/api/${path}/`, formData, {
		headers: {
			"X-CSRFToken": csrftoken,
			"Content-Type": contentType,
		},
	});
}

export default function usePostData() {
	return useMutation(postFormData);
}
