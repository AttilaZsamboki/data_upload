import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from "react";
import { Navigate } from "react-router-dom";
import { FormControl, Input, InputLabel } from "@mui/material";
import KeyboardArrowUpIcon from "@mui/icons-material/KeyboardArrowUp";
import Button from "@mui/material/Button";
import Userfront from "@userfront/react";
import { Autocomplete, TextField } from "@mui/material";
import { useColumnNames } from "../hooks/Templates";
import usePostData from "../hooks/general";
import { useTableOptions } from "../hooks/Tables";
export default function AddTemplate() {
    var _a;
    if (!Userfront.accessToken())
        return _jsx(Navigate, { to: '/login', replace: true });
    const appendOptions = ["Hozzáfűzés duplikációk szűrésével", "Hozzáfűzés", "Felülírás"];
    const formatOptions = ["xlsx", "csv", "tsv"];
    const tableOptions = useTableOptions();
    const [state, setState] = useState({});
    const [sourceColumns, setSourceColumns] = useState({});
    const columnNames = useColumnNames(state.table);
    const { mutate: postFormData, isSuccess } = usePostData();
    const handleChange = ({ target }) => {
        const { name, value } = target;
        setState((values) => (Object.assign(Object.assign({}, values), { [name]: value })));
    };
    const handleAddTemplate = () => {
        postFormData({
            path: "templates",
            formData: {
                table: state.table,
                pkey_col: state.pkey_col,
                skiprows: state.skiprows,
                created_by_id: Userfront.user.userId,
                append: state.append,
                source_column_names: JSON.stringify(sourceColumns),
            },
        });
    };
    return (_jsxs("div", Object.assign({ className: 'center-form all-white-bg' }, { children: [_jsx("h1", Object.assign({ className: 'bg-slate-200 pb-6' }, { children: "Template Hozz\u00E1ad\u00E1sa" })), _jsx(Autocomplete, { disablePortal: true, value: state.table, id: 'table', options: tableOptions.data, sx: { width: 300 }, renderInput: (params) => _jsx(TextField, Object.assign({}, params, { label: 'T\u00E1bla neve' })), onChange: (e, v) => setState((prev) => (Object.assign(Object.assign({}, prev), { table: v }))) }), _jsx("br", {}), _jsx(TextField, { type: 'number', name: 'skiprows', label: 'Kihagyott sorok sz\u00E1ma', value: state.skiprows, onChange: handleChange }), _jsx("br", {}), _jsxs(FormControl, { children: [_jsx(InputLabel, Object.assign({ htmlFor: 'pkey_col' }, { children: "Primary Key Column" })), _jsx(Input, { id: 'pkey_col', name: 'pkey_col', type: 'text', value: state.pkey_col, onChange: handleChange })] }), _jsx("br", {}), _jsx(Autocomplete, { disablePortal: true, id: 'appendOptions', name: 'appendOptions', type: 'text', options: appendOptions, sx: { width: 300 }, renderInput: (params) => _jsx(TextField, Object.assign({}, params, { label: 'Hoz\u00E1\u00E1f\u0171z\u00E9s form\u00E1ja' })), onChange: (e, v) => setState((prev) => (Object.assign(Object.assign({}, prev), { append: v }))), value: state.append }), _jsx("br", {}), columnNames.data && (_jsx("div", { children: (_a = columnNames.data) === null || _a === void 0 ? void 0 : _a.map((column) => (_jsxs(FormControl, { children: [_jsx(InputLabel, Object.assign({ htmlFor: column }, { children: column })), _jsx(Input, { id: column, name: column, type: 'text', onChange: ({ target }) => setSourceColumns((prev) => (Object.assign(Object.assign({}, prev), { [target.name]: target.value }))) })] }))) })), _jsx(Button, Object.assign({ onClick: handleAddTemplate, disabled: !columnNames, variant: 'contained', sx: {
                    "backgroundColor": "#057D55",
                    "&:hover": { color: "white" },
                }, endIcon: _jsx(KeyboardArrowUpIcon, {}), type: 'submit' }, { children: "Submit" })), isSuccess && _jsx(Navigate, { to: '/upload', replace: true })] })));
}
