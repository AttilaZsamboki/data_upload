import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useRef, useEffect } from "react";
import Userfront from "@userfront/react";
import { Navigate } from "react-router-dom";
import { Autocomplete } from "@mui/material";
import FileUploadIcon from "@mui/icons-material/FileUpload";
import { TextField, Box, Button } from "@mui/material";
import usePostData from "../hooks/general";
import { useTableOptions } from "../hooks/Tables";
export default function DataUpload() {
    if (!Userfront.accessToken())
        return _jsx(Navigate, { to: '/login' });
    const inputRef = useRef(null);
    const [inputTable, setInputTable] = useState();
    const [inputFile, setInputFile] = useState();
    const tableOptions = useTableOptions();
    const { mutate: postFormData, isSuccess } = usePostData();
    useEffect(() => {
        document.title = "Upload";
    }, []);
    const onFileUpload = (e) => {
        postFormData({
            path: "uploadmodel",
            formData: {
                table: inputTable,
                file: inputFile,
                user_id: Userfront.user.userId,
                is_new_table: false,
            },
        });
        if (isSuccess) {
            window.location.reload(false);
        }
    };
    return (_jsxs("form", Object.assign({ className: 'center-form', onSubmit: onFileUpload }, { children: [_jsx("h1", Object.assign({ className: 'pb-16' }, { children: "F\u00E1jl Felt\u00F6lt\u00E9se" })), _jsx("div", Object.assign({ className: 'flex justify-center' }, { children: _jsxs("div", Object.assign({ className: 'mb-3 w-96 object-left-top' }, { children: [_jsx("label", Object.assign({ htmlFor: 'formFile' }, { children: "V\u00E1lassz ki egy f\u00E1jlt (.xlsx, .csv, .tsv):" })), _jsx("input", { className: 'form-control\tblock w-full px-3 py-1.5 text-base font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none', type: 'file', id: 'formFile', onChange: (e) => setInputFile(e.target.files[0]) })] })) })), _jsx("br", {}), _jsx(Autocomplete, { className: 'bg-white col-span-1', disablePortal: true, id: 'table', name: 'table', type: 'text', options: tableOptions.data, sx: { width: 300 }, renderInput: (params) => _jsx(TextField, Object.assign({}, params, { label: 'T\u00E1bla neve' })), onChange: (e, values) => typeof values === "string" && setInputTable(values), value: inputTable && inputTable.replace((Userfront.user.name.slice(0, 3) + "_").toLowerCase(), ""), renderOption: (props, option) => (_jsx(Box, Object.assign({ component: 'li', sx: { "& > img": { mr: 2, flexShrink: 0 } } }, props, { children: option.replace((Userfront.user.name.slice(0, 3) + "_").toLowerCase(), "") }))) }), _jsx("br", {}), _jsx(Button, Object.assign({ disabled: !inputFile, variant: 'contained', className: '', sx: {
                    "backgroundColor": "#057D55",
                    "&:hover": { color: "white" },
                    "marginTop": 3,
                }, endIcon: _jsx(FileUploadIcon, {}), type: 'submit' }, { children: "Felt\u00F6lt\u00E9s" })), isSuccess && _jsx(Navigate, { to: '/upload', replace: true })] })));
}
