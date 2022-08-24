import axios from "axios";
import { useQuery } from "react-query";
import getCookie from "../utils/GetCookie";
export async function fetchColumnNames(table) {
    const response = await axios.get("/api/column-names");
    const filteredData = response.data
        .filter((column) => column[0] === table && column[1] !== "id")
        .map((column) => column[1]);
    return filteredData;
}
export function useColumnNames(table) {
    return useQuery(["column-names", table], () => {
        if (typeof table === "string") {
            return fetchColumnNames(table);
        }
    });
}
function addTemplate(formData) {
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
