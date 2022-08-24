import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import * as React from "react";
import { useTable, useTableOptions } from "../hooks/Tables";
import { Autocomplete, TextField, Button } from "@mui/material";
import Userfront from "@userfront/react";
import { Navigate } from "react-router-dom";
import getCookie from "../utils/GetCookie";
import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-material.css";
import { useState } from "react";
import { AgGridReact } from "ag-grid-react";
import { useEffect, useMemo } from "react";
import { Box } from "@mui/system";
import axios from "axios";
const csrftoken = getCookie("csrftoken");
function DataFrame({ importConfig }) {
    const gridRef = React.useRef();
    const [inputTable, setInputTable] = useState();
    const [columnDefs, setColumnDefs] = useState(null);
    const tables = useTableOptions();
    const table = useTable(inputTable);
    const importConfigTypes = ["Templates", "Special queries"];
    useEffect(() => {
        if (table.data && inputTable) {
            setColumnDefs(Object.keys(table.data[0]).map((col) => ({ field: col })));
        }
    }, [inputTable, table]);
    const defaultColDef = useMemo(() => ({
        floatingFilter: true,
        filter: true,
        minWidth: 200,
        editable: true,
        sortable: true,
        flex: 1,
        filterParams: {
            debounceMs: 0,
        },
    }), []);
    const onBtWhich = (event) => {
        axios.put(`/api/${inputTable.toLowerCase().replace(" ", "-")}/${event.data.id}/`, event.data, {
            headers: {
                "X-CSRFToken": csrftoken,
                "Content-Type": "multipart/form-data",
            },
        });
    };
    const getRowId = useMemo(() => {
        return (params) => {
            return params.data.id;
        };
    }, []);
    return (_jsxs("div", { children: [_jsx("h1", Object.assign({ className: 'flex flex-col items-center justify-center mb-3' }, { children: !importConfig ? "Adatok" : "Import Konfigurációk" })), _jsx(Autocomplete, { className: 'm-auto flex flex-col items-center justify-center', id: 'table', options: importConfig ? importConfigTypes : tables.data, sx: { width: 300 }, renderInput: (params) => _jsx(TextField, Object.assign({}, params, { label: importConfig ? "Konfig neve" : "Tábla neve" })), onChange: (e, v) => setInputTable(v) }), importConfig && typeof inputTable === "string" && (_jsx(Box, Object.assign({ textAlign: 'center', marginTop: 5 }, { children: _jsx(Button, Object.assign({ sx: {
                        "&:hover": { color: "white" },
                        "backgroundColor": "#057D55",
                    }, variant: 'contained', href: `/add-${inputTable.toLowerCase().replace(" ", "-")}`, disabled: !inputTable }, { children: `${inputTable ? inputTable.slice(0, -1) : ""} hozzáadása` })) }))), _jsx("div", Object.assign({ className: 'mx-auto flex flex-col items-center justify-center ' }, { children: _jsx("div", Object.assign({ className: 'ag-theme-material', style: { width: "92%", height: 700, marginTop: 50 } }, { children: _jsx(AgGridReact, { ref: gridRef, animateRows: true, defaultColDef: defaultColDef, rowSelection: "multiple", rowData: table.data, columnDefs: columnDefs, getRowId: getRowId, stopEditingWhenCellsLoseFocus: true, onCellValueChanged: onBtWhich }) })) }))] }));
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
