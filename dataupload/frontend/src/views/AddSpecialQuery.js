import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from "react";
import { Navigate } from "react-router-dom";
import { FormControl, Input, InputLabel, Button, Autocomplete, TextField } from "@mui/material";
import KeyboardArrowUpIcon from "@mui/icons-material/KeyboardArrowUp";
import Userfront from "@userfront/react";
import { useTableOptions } from "../hooks/Tables";
import usePostData from "../hooks/general";
export default function addSpecialQueries() {
    if (!Userfront.accessToken())
        return _jsx(Navigate, { to: '/login', replace: true });
    const tables = useTableOptions();
    const { mutate: postFormData, isSuccess } = usePostData();
    const [state, setState] = useState({
        special_query: "",
        created_by_id: Userfront.user.userId,
        table: null,
        name: "",
    });
    const handleAddSpecialQuery = () => {
        postFormData({
            path: "special-queries",
            formData: {
                special_query: state.special_query,
                created_by_id: Userfront.user.userId,
                table: state.table,
                name: state.name,
            },
        });
    };
    if (tables.isLoading)
        return _jsx("span", { children: "Loading..." });
    if (tables.isError)
        return _jsxs("span", { children: ["Error: ", tables.error.message] });
    return (_jsxs("div", Object.assign({ className: 'center-form all-white-bg mb-5 w-auto px-10' }, { children: [_jsx("h1", Object.assign({ className: 'bg-slate-200 pb-6' }, { children: "Speci\u00E1lis Query Hozz\u00E1ad\u00E1sa" })), _jsxs(FormControl, { children: [_jsx(InputLabel, Object.assign({ htmlFor: 'name' }, { children: "Query Neve" })), _jsx(Input, { className: 'better-base-input', id: 'name', name: 'name', type: 'text', onChange: (e) => setState((prev) => (Object.assign(Object.assign({}, prev), { name: e.target.value }))), value: state.name })] }), _jsx("br", {}), _jsx(Autocomplete, { disablePortal: true, id: 'table', options: tables.data, sx: { width: 300 }, onChange: (e, v) => setState((prev) => (Object.assign(Object.assign({}, prev), { table: v }))), value: state.table, renderInput: (params) => _jsx(TextField, Object.assign({}, params, { label: 'T\u00E1bla neve' })) }), _jsx("br", {}), _jsx(TextField, { id: 'special-query', label: 'Speci\u00E1lis query', multiline: true, rows: 8, fullWidth: true, value: state.special_query, onChange: (e) => setState((prev) => (Object.assign(Object.assign({}, prev), { special_query: e.target.value }))) }), _jsx("br", {}), _jsx(Button, Object.assign({ onClick: handleAddSpecialQuery, variant: 'contained', sx: {
                    "backgroundColor": "#057D55",
                    "&:hover": { color: "white" },
                }, endIcon: _jsx(KeyboardArrowUpIcon, {}), type: 'submit' }, { children: "Submit" })), isSuccess && _jsx(Navigate, { to: '/upload', replace: true })] })));
}
