import { jsx as _jsx, jsxs as _jsxs, Fragment as _Fragment } from "react/jsx-runtime";
import { useTable, useTableOptions } from "../hooks/Tables";
import { Autocomplete, TextField, Button } from "@mui/material";
import Userfront from "@userfront/react";
import { Navigate } from "react-router-dom";
import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-alpine.css";
import { useState } from "react";
import { AgGridReact } from "ag-grid-react";
import { useEffect, useMemo } from "react";
function DataFrame({ importConfig }) {
    const [inputTable, setInputTable] = useState();
    const [columnDefs, setColumnDefs] = useState(null);
    const tables = importConfig ? { data: ["Templates", "Special queries"] } : useTableOptions();
    const table = typeof inputTable === "string" && useTable(inputTable);
    useEffect(() => {
        if (table.data) {
            setColumnDefs(Object.keys(table.data[0]).map((col) => ({ field: col })));
        }
    }, [table]);
    const defaultColDef = useMemo(() => ({
        floatingFilter: true,
        filter: true,
        minWidth: 200,
        flex: 1,
        filterParams: {
            debounceMs: 0,
        },
    }), []);
    if (tables.isLoading)
        return _jsx("span", { children: "Loading..." });
    if (tables.isError)
        return _jsxs("span", { children: ["Error: ", tables.error.message] });
    return (_jsxs(_Fragment, { children: [_jsx(Autocomplete, { id: 'table', options: tables.data, sx: { width: 300 }, renderInput: (params) => _jsx(TextField, Object.assign({}, params, { label: "Table name" })), onChange: (e, v) => setInputTable(v) }), importConfig && (_jsx(Button, Object.assign({ variant: 'contained', href: `/add-${inputTable.toLowerCase()}/`, disabled: !inputTable }, { children: `Add-${inputTable ? inputTable : ""}` }))), _jsx("div", Object.assign({ className: 'ag-theme-alpine', style: { width: "100%", height: 700, marginTop: 50 } }, { children: _jsx(AgGridReact, { defaultColDef: defaultColDef, rowSelection: "multiple", rowData: table.data, columnDefs: columnDefs }) }))] }));
}
export function Adatok() {
    if (!Userfront.accessToken()) {
        return _jsx(Navigate, { to: '/login' });
    }
    useEffect(() => {
        document.title = "Adatok";
    }, []);
    return _jsx(DataFrame, { importConfig: false });
}
export function ImportConfig() {
    if (!Userfront.accessToken()) {
        return _jsx(Navigate, { to: '/login' });
    }
    useEffect(() => {
        document.title = "ImportConfig";
    }, []);
    return _jsx(DataFrame, { importConfig: true });
}
