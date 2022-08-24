import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from "react";
import Userfront from "@userfront/react";
import { Navigate } from "react-router-dom";
import AddIcon from "@mui/icons-material/Add";
import { FormControl, Input, InputLabel, Button, Autocomplete, TextField } from "@mui/material";
import usePostData from "../hooks/general";
export default function CreateTable() {
    if (!Userfront.accessToken()) {
        return _jsx(Navigate, { to: '/login' });
    }
    else if (!["dark-frost-2k269", "winter-salad-brlnr", "ancient-river-26kn4"].includes(Userfront.user.username)) {
        return _jsx(Navigate, { to: '/upload' });
    }
    const { mutate: postFormData, isSuccess, error } = usePostData();
    const formatOptions = ["xlsx", "csv", "tsv"];
    const [inputTable, setInputTable] = useState(null);
    const [selectedFile, setSelectedFile] = useState(null);
    const [format, setFormat] = useState(null);
    const [skiprows, setSkiprows] = useState(null);
    const onFileUpload = () => {
        postFormData({
            path: "uploadmodel",
            formData: {
                table: inputTable,
                file: selectedFile,
                user_id: Userfront.user.userId,
                is_new_table: true,
                skiprows: skiprows,
            },
        });
    };
    return (_jsxs("div", Object.assign({ className: 'center-form mx-80 py-20 my-32' }, { children: [_jsx("div", Object.assign({ className: 'flex justify-center' }, { children: _jsxs("div", Object.assign({ className: 'mb-3 w-96 object-left-top' }, { children: [_jsx("label", Object.assign({ htmlFor: 'formFile' }, { children: "V\u00E1lassz ki egy f\u00E1jlt:" })), _jsx("input", { className: 'form-control\tblock w-full px-3 py-1.5 text-base font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none', type: 'file', id: 'formFile', onChange: (e) => setSelectedFile(e.target.files[0]) })] })) })), _jsx("br", {}), _jsx(Autocomplete, { className: 'bg-white', disablePortal: true, id: 'format', options: formatOptions, sx: { width: 300 }, renderInput: (params) => _jsx(TextField, Object.assign({}, params, { label: 'F\u00E1jlform\u00E1tum' })), onChange: (event, values) => setFormat(values) }), _jsx("br", {}), _jsxs(FormControl, { children: [_jsx(InputLabel, Object.assign({ htmlFor: 'table' }, { children: "T\u00E1bla neve" })), _jsx(Input, { className: 'better-base-input bg-white', sx: { height: 50 }, id: 'table', name: 'table', type: 'text', value: inputTable, onChange: ({ target }) => setInputTable(target.value) })] }), _jsx("br", {}), _jsx(TextField, { type: 'number', className: 'bg-white', name: 'skiprows', label: 'Kihagyott sorok sz\u00E1ma', value: skiprows, onChange: ({ target }) => setSkiprows(target.value) }), _jsx("br", {}), _jsx(Button, Object.assign({ onClick: onFileUpload, variant: 'contained', sx: {
                    "backgroundColor": "#057D55",
                    "&:hover": { color: "white" },
                }, endIcon: _jsx(AddIcon, {}), type: 'submit' }, { children: "L\u00E9trehoz\u00E1s" })), isSuccess && _jsx(Navigate, { to: '/upload', replace: true })] })));
}
