import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect, useRef } from "react";
import Userfront from "@userfront/react";
import { Navigate } from "react-router-dom";
import getCookie from "../utils/GetCookie";
import AddIcon from "@mui/icons-material/Add";
import { FormControl, Input, InputLabel, Button, FormHelperText, Autocomplete, TextField } from "@mui/material";
import axios from "axios";
export default function SpecialQueries() {
    if (!Userfront.accessToken()) {
        return _jsx(Navigate, { to: '/login' });
    }
    else if (!["dark-frost-2k269", "winter-salad-brlnr", "ancient-river-26kn4"].includes(Userfront.user.username)) {
        return _jsx(Navigate, { to: '/upload' });
    }
    const formatOptions = ["xlsx", "csv", "tsv"];
    const inputRef = useRef(null);
    const csrftoken = getCookie("csrftoken");
    const [inputTable, setInputTable] = useState(null);
    const [selectedFile, setSelectedFile] = useState(null);
    const [format, setFormat] = useState(null);
    const [skiprows, setSkiprows] = useState(null);
    const [isFinished, setIsFinished] = useState(false);
    useEffect(() => {
        document.title = "Tábla létrehozás";
    });
    const onFileUpload = (event) => {
        const tablePrefix = Userfront.user.name.toLowerCase().slice(0, 3) + "_";
        event.preventDefault();
        const formData = new FormData();
        formData.append("table", tablePrefix + inputTable);
        formData.append("file", selectedFile);
        formData.append("user_id", Userfront.user.userId);
        formData.append("is_new_table", true);
        formData.append("extension_format", format);
        formData.append("skiprows", skiprows);
        axios({
            method: "post",
            url: "/api/uploadmodel/",
            data: formData,
            headers: {
                "X-CSRFToken": csrftoken,
                "Content-Type": "multipart/form-data",
            },
        });
        setInputTable(null);
        setIsFinished(true);
        inputRef.current.value = null;
    };
    const formControlStyle = {
        marginBottom: 20,
        width: 200,
    };
    return (_jsx("div", { children: _jsxs("form", Object.assign({ onSubmit: onFileUpload }, { children: [_jsxs(FormControl, Object.assign({ style: formControlStyle }, { children: [_jsx(InputLabel, Object.assign({ htmlFor: 'table' }, { children: "T\u00E1bla neve" })), _jsx(Input, { id: 'table', name: 'table', type: 'text', value: inputTable, onChange: ({ target }) => setInputTable(target.value) })] })), _jsx("br", {}), _jsx(Autocomplete, { disablePortal: true, id: 'format', options: formatOptions, sx: { width: 300 }, renderInput: (params) => _jsx(TextField, Object.assign({}, params, { label: 'F\u00E1jlform\u00E1tum' })), onChange: (event, values) => setFormat(values) }), _jsx("br", {}), _jsx(TextField, { type: 'number', name: 'skiprows', label: 'Kihagyott sorok sz\u00E1ma', value: skiprows, onChange: ({ target }) => setSkiprows(target.value) }), _jsx("br", {}), _jsxs(FormControl, Object.assign({ style: formControlStyle }, { children: [_jsx("input", { id: 'file', name: 'file', type: 'file', onChange: ({ target }) => setSelectedFile(target.files[0]), ref: inputRef }), _jsx(FormHelperText, { children: "P\u00E9lda File" })] })), _jsx("br", {}), _jsx(Button, Object.assign({ variant: 'contained', sx: {
                        "backgroundColor": "#057D55",
                        "&:hover": { color: "white" },
                    }, endIcon: _jsx(AddIcon, {}), type: 'submit' }, { children: "L\u00E9trehoz\u00E1s" })), isFinished && _jsx(Navigate, { to: '/upload', replace: true })] })) }));
}
