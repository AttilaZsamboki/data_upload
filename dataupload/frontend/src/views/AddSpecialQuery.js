import { jsx as _jsx, jsxs as _jsxs, Fragment as _Fragment } from "react/jsx-runtime";
import { useState } from "react";
import { Navigate } from "react-router-dom";
import { FormControl, Input, InputLabel, Button, Autocomplete, TextField } from "@mui/material";
import KeyboardArrowUpIcon from "@mui/icons-material/KeyboardArrowUp";
import Userfront from "@userfront/react";
import { useTableOptions } from "../hooks/Tables";
import useCreateSpecialQuery from "../hooks/SpecialQueries";
export default function addSpecialQueries() {
    if (!Userfront.accessToken())
        return _jsx(Navigate, { to: '/login', replace: true });
    const tables = useTableOptions();
    const { mutate: addSpecialQuery, isSuccess } = useCreateSpecialQuery();
    const [state, setState] = useState({
        special_query: "",
        created_by_id: Userfront.user.userId,
        table: "",
        name: "",
    });
    const handleAddSpecialQuery = () => {
        // addSpecialQuery({
        // 	special_query: state.special_query,
        // 	created_by_id: Userfront.user.userId,
        // 	table: state.table,
        // 	name: state.name,
        // });
        console.log(state);
    };
    if (tables.isLoading)
        return _jsx("span", { children: "Loading..." });
    if (tables.isError)
        return _jsxs("span", { children: ["Error: ", tables.error.message] });
    return (_jsx(_Fragment, { children: _jsxs("div", Object.assign({ style: { marginBottom: 20, width: 500 } }, { children: [_jsxs(FormControl, { children: [_jsx(InputLabel, Object.assign({ htmlFor: 'name' }, { children: "Query Name" })), _jsx(Input, { id: 'name', name: 'name', type: 'text', onChange: (e) => setState((prev) => (Object.assign(Object.assign({}, prev), { name: e.target.value }))), value: state.name })] }), _jsx("br", {}), _jsx(Autocomplete, { disablePortal: true, id: 'table', options: tables.data, sx: { width: 300 }, onChange: (e, v) => setState((prev) => (Object.assign(Object.assign({}, prev), { table: v }))), value: state.table, renderInput: (params) => _jsx(TextField, Object.assign({}, params, { label: 'T\u00E1bla neve' })) }), _jsx("br", {}), _jsx(TextField, { id: 'special-query', label: 'Special SQL query', multiline: true, rows: 8, fullWidth: true, value: state.special_query, onChange: (e) => setState((prev) => (Object.assign(Object.assign({}, prev), { special_query: e.target.value }))) }), _jsx("br", {}), _jsx(Button, Object.assign({ onClick: handleAddSpecialQuery, variant: 'contained', sx: {
                        "backgroundColor": "#057D55",
                        "&:hover": { color: "white" },
                    }, endIcon: _jsx(KeyboardArrowUpIcon, {}), type: 'submit' }, { children: "Submit" }))] })) }));
}
