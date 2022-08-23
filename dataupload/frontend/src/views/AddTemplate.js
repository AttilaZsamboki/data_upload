import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from "react";
import { Navigate } from "react-router-dom";
import { FormControl, Input, InputLabel } from "@mui/material";
import KeyboardArrowUpIcon from "@mui/icons-material/KeyboardArrowUp";
import Button from "@mui/material/Button";
import Userfront from "@userfront/react";
import { Autocomplete, TextField } from "@mui/material";
import { useColumnNames, useCreateTemplate } from "../hooks/Templates";
import { useTableOptions } from "../hooks/Tables";
export default function AddTemplate() {
    if (!Userfront.accessToken())
        return _jsx(Navigate, { to: '/login', replace: true });
    const appendOptions = ["Hozzáfűzés duplikációk szűrésével", "Hozzáfűzés", "Felülírás"];
    const formatOptions = ["xlsx", "csv", "tsv"];
    const tableOptions = useTableOptions();
    const [state, setState] = useState({});
    const columnNames = useColumnNames(state.table);
    const { mutate: addTemplate, isSuccess } = useCreateTemplate();
    const handleChange = ({ target }) => {
        const { name, value } = target;
        setState((values) => (Object.assign(Object.assign({}, values), { [name]: value })));
    };
    const handleAddTemplate = () => {
        // addTemplate({
        // 	table: state.table,
        // 	pkey_col: state.pkey_col,
        // 	skiprows: state.skiprows,
        // 	created_by_id: Userfront.user.userId,
        // 	append: state.append,
        // 	extension_format: state.extension_format,
        // 	source_column_names: state.source_column_names,
        // });
        console.log({ state });
    };
    return (_jsxs("div", { children: [_jsx(Autocomplete, { disablePortal: true, value: state.table, id: 'table', options: tableOptions.data, sx: { width: 300 }, renderInput: (params) => _jsx(TextField, Object.assign({}, params, { label: 'T\u00E1bla neve' })), onChange: (e, v) => setState((prev) => (Object.assign(Object.assign({}, prev), { table: v }))) }), _jsx("br", {}), _jsx(TextField, { type: 'number', name: 'skiprows', label: 'Kihagyott sorok sz\u00E1ma', value: state.skiprows, onChange: handleChange }), _jsx("br", {}), _jsxs(FormControl, { children: [_jsx(InputLabel, Object.assign({ htmlFor: 'primaryKeyColumn' }, { children: "Primary Key Column" })), _jsx(Input, { id: 'primaryKeyColumn', name: 'primaryKeyColumn', type: 'text', value: state.pkey_col, onChange: handleChange })] }), _jsx("br", {}), _jsx(Autocomplete, { disablePortal: true, id: 'appendOptions', name: 'appendOptions', type: 'text', options: appendOptions, sx: { width: 300 }, renderInput: (params) => _jsx(TextField, Object.assign({}, params, { label: 'Hoz\u00E1\u00E1f\u0171z\u00E9s form\u00E1ja' })), onChange: (e, v) => setState((prev) => (Object.assign(Object.assign({}, prev), { append: v }))), value: state.append }), _jsx("br", {}), _jsx(Autocomplete, { disablePortal: true, id: 'format', options: formatOptions, sx: { width: 300 }, renderInput: (params) => _jsx(TextField, Object.assign({}, params, { label: 'F\u00E1jlform\u00E1tum' })), onChange: (e, v) => setState((prev) => (Object.assign(Object.assign({}, prev), { extension_format: v }))), value: state.extension_format }), _jsx("br", {}), columnNames && (_jsx("div", { children: columnNames.data.map((column) => (_jsxs(FormControl, { children: [_jsx(InputLabel, Object.assign({ htmlFor: column }, { children: column })), _jsx(Input, { id: column, name: column, type: 'text', onChange: handleChange })] }))) })), _jsx(Button, Object.assign({ onClick: handleAddTemplate, disabled: !columnNames, variant: 'contained', sx: {
                    "backgroundColor": "#057D55",
                    "&:hover": { color: "white" },
                }, endIcon: _jsx(KeyboardArrowUpIcon, {}), type: 'submit' }, { children: "Submit" })), isSuccess && _jsx(Navigate, { to: '/upload', replace: true })] }));
}
