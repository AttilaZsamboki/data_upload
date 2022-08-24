import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import * as React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import DataUpload from "./views/DataUpload";
import HomePage from "./views/HomePage";
import Signup from "./views/SignupPage";
import PwdReset from "./views/PasswordReset";
import Login from "./views/LoginPage";
import { Adatok, ImportConfig } from "./views/DataFrame";
import CssBaseline from "@mui/material/CssBaseline";
import NavBar from "./components/NavBar";
import AddTemplate from "./views/AddTemplate";
import AddSpecialQueries from "./views/AddSpecialQuery";
import Footer from "./components/Footer";
import CreateTable from "./views/CreateTable";
import { QueryClient, QueryClientProvider } from "react-query";
import { ReactQueryDevtools } from "react-query/devtools";
const queryClient = new QueryClient();
function App() {
    return (_jsx(React.Fragment, { children: _jsxs(QueryClientProvider, Object.assign({ client: queryClient }, { children: [_jsx(CssBaseline, { enableColorScheme: true }), _jsxs(BrowserRouter, { children: [_jsx(NavBar, {}), _jsxs(Routes, { children: [_jsx(Route, { path: '/adatok', element: _jsx(Adatok, {}) }), _jsx(Route, { path: '/login', element: _jsx(Login, {}) }), _jsx(Route, { path: '/reset', element: _jsx(PwdReset, {}) }), _jsx(Route, { path: '/signup', element: _jsx(Signup, {}) }), _jsx(Route, { path: '/upload', element: _jsx(DataUpload, {}) }), _jsx(Route, { path: '/', element: _jsx(HomePage, {}) }), _jsx(Route, { path: '/add-templates', element: _jsx(AddTemplate, {}) }), _jsx(Route, { path: '/import-config', element: _jsx(ImportConfig, {}) }), _jsx(Route, { path: '/add-special-queries', element: _jsx(AddSpecialQueries, {}) }), _jsx(Route, { path: '/create-table', element: _jsx(CreateTable, {}) })] })] }), _jsx(Footer, {}), _jsx(ReactQueryDevtools, { initialIsOpen: false })] })) }));
}
export default App;
