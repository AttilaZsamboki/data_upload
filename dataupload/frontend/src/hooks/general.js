import getCookie from "../utils/GetCookie";
import axios from "axios";
import { useMutation } from "react-query";
function postFormData({ path, formData }) {
    const csrftoken = getCookie("csrftoken");
    axios
        .post(`/api/${path}/`, formData, {
        headers: {
            "X-CSRFToken": csrftoken,
            "Content-Type": "multipart/form-data",
        },
    })
        .then((res) => res.data);
}
export default function usePostData() {
    return useMutation(postFormData);
}
