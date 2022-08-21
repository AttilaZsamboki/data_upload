import { jsx as _jsx, Fragment as _Fragment, jsxs as _jsxs } from "react/jsx-runtime";
import * as React from "react";
import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import Toolbar from "@mui/material/Toolbar";
import IconButton from "@mui/material/IconButton";
import Typography from "@mui/material/Typography";
import Menu from "@mui/material/Menu";
import MenuIcon from "@mui/icons-material/Menu";
import Container from "@mui/material/Container";
import Avatar from "@mui/material/Avatar";
import Tooltip from "@mui/material/Tooltip";
import MenuItem from "@mui/material/MenuItem";
import Button from "@mui/material/Button";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import Userfront from "@userfront/core";
import LogoutButton from "./Auth";
const pages = ["Adatok", "Import config"];
const settings = [
    "Profile",
    "Account",
    "Settings",
    Userfront.accessToken() ? (_jsx(LogoutButton, {})) : (_jsx(Button, Object.assign({ variant: 'contained', href: '/login', sx: { "&:hover": { color: "white" } } }, { children: "Login" }))),
];
const NavBar = () => {
    const [anchorElNav, setAnchorElNav] = React.useState(null);
    const [anchorElUser, setAnchorElUser] = React.useState(null);
    const handleOpenNavMenu = (event) => {
        setAnchorElNav(event.currentTarget);
    };
    const handleOpenUserMenu = (event) => {
        setAnchorElUser(event.currentTarget);
    };
    const handleCloseNavMenu = () => {
        setAnchorElNav(null);
    };
    const handleCloseUserMenu = () => {
        setAnchorElUser(null);
    };
    return (_jsx(AppBar, Object.assign({ position: 'static', sx: { marginBottom: 5, backgroundColor: "#013970" } }, { children: _jsx(Container, Object.assign({ maxWidth: 'xl' }, { children: _jsxs(Toolbar, Object.assign({ disableGutters: true }, { children: [_jsx(CloudUploadIcon, { sx: { display: { xs: "none", md: "flex" }, mr: 1 } }), _jsx(Typography, Object.assign({ variant: 'h6', noWrap: true, component: 'a', href: '/upload', sx: {
                            "mr": 2,
                            "display": { xs: "none", md: "flex" },
                            "fontFamily": "monospace",
                            "fontWeight": 700,
                            "letterSpacing": ".3rem",
                            "color": "inherit",
                            "textDecoration": "none",
                            "&:hover": { color: "#04010A" },
                        } }, { children: "UPLOAD" })), _jsxs(Box, Object.assign({ sx: { flexGrow: 1, display: { xs: "flex", md: "none" } } }, { children: [_jsx(IconButton, Object.assign({ size: 'large', "aria-label": 'account of current user', "aria-controls": 'menu-appbar', "aria-haspopup": 'true', onClick: handleOpenNavMenu, color: 'inherit' }, { children: _jsx(MenuIcon, {}) })), _jsxs(Menu, Object.assign({ id: 'menu-appbar', anchorEl: anchorElNav, anchorOrigin: {
                                    vertical: "bottom",
                                    horizontal: "left",
                                }, keepMounted: true, transformOrigin: {
                                    vertical: "top",
                                    horizontal: "left",
                                }, open: Boolean(anchorElNav), onClose: handleCloseNavMenu, sx: {
                                    display: { xs: "block", md: "none" },
                                } }, { children: [pages.map((page) => (_jsx(MenuItem, Object.assign({ onClick: handleCloseNavMenu }, { children: _jsx(Typography, Object.assign({ textAlign: 'center' }, { children: _jsx(Button, Object.assign({ href: `/${page.toLowerCase().replace(" ", "-")}` }, { children: page })) })) }), page))), ["dark-frost-2k269", "winter-salad-brlnr", "ancient-river-26kn4"].includes(Userfront.user.username) && (_jsxs(_Fragment, { children: [_jsx(MenuItem, Object.assign({ onClick: handleCloseNavMenu }, { children: _jsx(Typography, Object.assign({ textAlign: 'center' }, { children: _jsx(Button, Object.assign({ href: "/create-table" }, { children: "T\u00E1bla l\u00E9trehoz\u00E1sa" })) })) }), 'create-table'), _jsx(MenuItem, Object.assign({ onClick: handleCloseNavMenu }, { children: _jsx(Typography, Object.assign({ textAlign: 'center' }, { children: _jsx(Button, Object.assign({ onClick: handleCloseNavMenu, href: "/signup" }, { children: "Felhaszn\u00E1l\u00F3 regisztr\u00E1l\u00E1sa" })) })) }), 'signup')] }))] }))] })), _jsx(CloudUploadIcon, { sx: { display: { xs: "flex", md: "none" }, mr: 1 } }), _jsx(Typography, Object.assign({ variant: 'h5', noWrap: true, component: 'a', href: '/upload', sx: {
                            "mr": 2,
                            "display": { xs: "flex", md: "none" },
                            "flexGrow": 1,
                            "fontFamily": "monospace",
                            "fontWeight": 700,
                            "letterSpacing": ".3rem",
                            "color": "inherit",
                            "textDecoration": "none",
                            "&:hover": { color: "#04010A" },
                        } }, { children: "UPLOAD" })), _jsxs(Box, Object.assign({ sx: { flexGrow: 1, display: { xs: "none", md: "flex" } } }, { children: [pages.map((page) => (_jsx(Button, Object.assign({ onClick: handleCloseNavMenu, sx: { "my": 2, "color": "white", "display": "block", "&:hover": { color: "#04010A" } }, href: `/${page.toLowerCase().replace(" ", "-")}` }, { children: page }), page))), ["dark-frost-2k269", "winter-salad-brlnr", "ancient-river-26kn4"].includes(Userfront.user.username) && (_jsxs(_Fragment, { children: [_jsx(Button, Object.assign({ onClick: handleCloseNavMenu, sx: {
                                            "my": 2,
                                            "color": "white",
                                            "display": "block",
                                            "&:hover": { color: "#04010A" },
                                        }, href: "/create-table" }, { children: "T\u00E1bla l\u00E9trehoz\u00E1sa" }), 'T\u00E1bla l\u00E9trehoz\u00E1sa'), _jsx(Button, Object.assign({ onClick: handleCloseNavMenu, sx: {
                                            "my": 2,
                                            "color": "white",
                                            "display": "block",
                                            "&:hover": { color: "#04010A" },
                                        }, href: "/signup" }, { children: "Felhaszn\u00E1l\u00F3 regisztr\u00E1l\u00E1sa" }), 'Felhaszn\u00E1l\u00F3 regisztr\u00E1l\u00E1sa')] }))] })), _jsxs(Box, Object.assign({ sx: { flexGrow: 0 } }, { children: [_jsx(Tooltip, Object.assign({ title: 'Open settings' }, { children: _jsx(IconButton, Object.assign({ onClick: handleOpenUserMenu, sx: { p: 0 } }, { children: _jsx(Avatar, { alt: 'Remy Sharp', src: '/static/images/avatar/2.jpg' }) })) })), _jsx(Menu, Object.assign({ sx: { mt: "45px" }, id: 'menu-appbar', anchorEl: anchorElUser, anchorOrigin: {
                                    vertical: "top",
                                    horizontal: "right",
                                }, keepMounted: true, transformOrigin: {
                                    vertical: "top",
                                    horizontal: "right",
                                }, open: Boolean(anchorElUser), onClose: handleCloseUserMenu }, { children: settings.map((setting) => (_jsx(MenuItem, Object.assign({ onClick: handleCloseUserMenu }, { children: _jsx(Typography, Object.assign({ textAlign: 'center' }, { children: setting })) }), setting))) }))] }))] })) })) })));
};
export default NavBar;
