import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import * as React from "react";
import Userfront from "@userfront/react";
import { styled, useTheme } from "@mui/material/styles";
import Box from "@mui/material/Box";
import MuiDrawer from "@mui/material/Drawer";
import MuiAppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import List from "@mui/material/List";
import CssBaseline from "@mui/material/CssBaseline";
import Typography from "@mui/material/Typography";
import Divider from "@mui/material/Divider";
import IconButton from "@mui/material/IconButton";
import MenuIcon from "@mui/icons-material/Menu";
import ChevronLeftIcon from "@mui/icons-material/ChevronLeft";
import ChevronRightIcon from "@mui/icons-material/ChevronRight";
import ListItem from "@mui/material/ListItem";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemIcon from "@mui/material/ListItemIcon";
import ListItemText from "@mui/material/ListItemText";
import UploadFileIcon from "@mui/icons-material/UploadFile";
import StorageIcon from "@mui/icons-material/Storage";
import ImportExportIcon from "@mui/icons-material/ImportExport";
import TableViewIcon from "@mui/icons-material/TableView";
import AssignmentIndIcon from "@mui/icons-material/AssignmentInd";
import AccountCircleSharpIcon from "@mui/icons-material/AccountCircleSharp";
import LogoutButton from "./Auth";
import LogoutIcon from "@mui/icons-material/Logout";
import { Link } from "react-router-dom";
import LoginIcon from "@mui/icons-material/Login";
const drawerWidth = 280;
const openedMixin = (theme) => ({
    width: drawerWidth,
    transition: theme.transitions.create("width", {
        easing: theme.transitions.easing.sharp,
        duration: theme.transitions.duration.enteringScreen,
    }),
    overflowX: "hidden",
});
const closedMixin = (theme) => ({
    transition: theme.transitions.create("width", {
        easing: theme.transitions.easing.sharp,
        duration: theme.transitions.duration.leavingScreen,
    }),
    overflowX: "hidden",
    width: `calc(${theme.spacing(7)} + 1px)`,
    [theme.breakpoints.up("sm")]: {
        width: `calc(${theme.spacing(8)} + 1px)`,
    },
});
const DrawerHeader = styled("div")(({ theme }) => (Object.assign({ display: "flex", alignItems: "center", justifyContent: "flex-end", padding: theme.spacing(0, 1) }, theme.mixins.toolbar)));
const AppBar = styled(MuiAppBar, {
    shouldForwardProp: (prop) => prop !== "open",
})(({ theme, open }) => (Object.assign({ zIndex: theme.zIndex.drawer + 1, transition: theme.transitions.create(["width", "margin"], {
        easing: theme.transitions.easing.sharp,
        duration: theme.transitions.duration.leavingScreen,
    }) }, (open && {
    marginLeft: drawerWidth,
    width: `calc(100% - ${drawerWidth}px)`,
    transition: theme.transitions.create(["width", "margin"], {
        easing: theme.transitions.easing.sharp,
        duration: theme.transitions.duration.enteringScreen,
    }),
}))));
const Drawer = styled(MuiDrawer, { shouldForwardProp: (prop) => prop !== "open" })(({ theme, open }) => (Object.assign(Object.assign({ width: drawerWidth, flexShrink: 0, whiteSpace: "nowrap", boxSizing: "border-box" }, (open && Object.assign(Object.assign({}, openedMixin(theme)), { "& .MuiDrawer-paper": openedMixin(theme) }))), (!open && Object.assign(Object.assign({}, closedMixin(theme)), { "& .MuiDrawer-paper": closedMixin(theme) })))));
export default function MiniDrawer() {
    const sideBar = ["dark-frost-2k269", "winter-salad-brlnr", "ancient-river-26kn4"].includes(Userfront.user.username)
        ? {
            upper: {
                "Upload": { href: "/upload/", icon: _jsx(UploadFileIcon, {}) },
                "Adatok": { href: "/adatok/", icon: _jsx(StorageIcon, {}) },
                "Import Konfig": { href: "/import-config/", icon: _jsx(ImportExportIcon, {}) },
                "Tábla Létrehozása": { href: "/create-table/", icon: _jsx(TableViewIcon, {}) },
                "Felhasználó Hozzáadása": { href: "/signup/", icon: _jsx(AssignmentIndIcon, {}) },
            },
            lower: {
                Fiók: { href: "/upload", icon: _jsx(AccountCircleSharpIcon, {}) },
                Kijelentkezés: {
                    href: "/login",
                    icon: (_jsx(LogoutIcon, { onClick: (event) => {
                            event.preventDefault();
                            Userfront.logout();
                        } })),
                },
            },
        }
        : Userfront.accessToken()
            ? {
                upper: {
                    Upload: { href: "/upload/", icon: _jsx(UploadFileIcon, {}) },
                    Adatok: { href: "/adatok/", icon: _jsx(StorageIcon, {}) },
                },
                lower: {
                    Fiók: { href: "/upload", icon: _jsx(AccountCircleSharpIcon, {}) },
                    Kijelentkezés: {
                        href: "/login",
                        icon: (_jsx(LogoutIcon, { onClick: (event) => {
                                event.preventDefault();
                                Userfront.logout();
                            } })),
                    },
                },
            }
            : { upper: { Bejelentkezés: { href: "/login/", icon: _jsx(LoginIcon, {}) } }, lower: {} };
    const theme = useTheme();
    const [open, setOpen] = React.useState(false);
    React.useEffect(() => {
        setOpen(JSON.parse(window.sessionStorage.getItem("open")));
    }, []);
    React.useEffect(() => {
        window.sessionStorage.setItem("open", open);
    }, [open]);
    const handleDrawerOpen = () => {
        setOpen(true);
    };
    const handleDrawerClose = () => {
        setOpen(false);
    };
    return (_jsxs(Box, Object.assign({ sx: { display: "flex", marginBottom: 20 } }, { children: [_jsx(CssBaseline, {}), _jsx(AppBar, Object.assign({ position: 'fixed', open: open, sx: { backgroundColor: "#013970" } }, { children: _jsxs(Toolbar, { children: [_jsx(IconButton, Object.assign({ color: 'inherit', "aria-label": 'open drawer', onClick: handleDrawerOpen, edge: 'start', sx: Object.assign({ marginRight: 5 }, (open && { display: "none" })) }, { children: _jsx(MenuIcon, {}) })), _jsx(Typography, Object.assign({ variant: 'h6', noWrap: true, component: 'div' }, { children: "Adatfelt\u00F6lt\u00E9s" }))] }) })), _jsxs(Drawer, Object.assign({ variant: 'permanent', open: open, sx: { marginLeft: 10 } }, { children: [_jsx(DrawerHeader, { children: _jsx(IconButton, Object.assign({ onClick: handleDrawerClose }, { children: theme.direction === "rtl" ? _jsx(ChevronRightIcon, {}) : _jsx(ChevronLeftIcon, {}) })) }), _jsx(Divider, {}), _jsx(List, { children: Object.keys(sideBar.upper).map((text) => (_jsx(Link, Object.assign({ to: sideBar.upper[text].href }, { children: _jsx(ListItem, Object.assign({ disablePadding: true, sx: { display: "block" } }, { children: _jsxs(ListItemButton, Object.assign({ sx: {
                                        minHeight: 48,
                                        justifyContent: open ? "initial" : "center",
                                        px: 2.5,
                                    } }, { children: [_jsx(ListItemIcon, Object.assign({ sx: {
                                                minWidth: 0,
                                                mr: open ? 3 : "auto",
                                                justifyContent: "center",
                                            } }, { children: sideBar.upper[text].icon })), _jsx(ListItemText, { primary: text, sx: { color: "gray", opacity: open ? 1 : 0 } })] })) }), text) })))) }), _jsx(Divider, {}), _jsx(List, { children: Object.keys(sideBar.lower).map((text) => (_jsx(ListItem, Object.assign({ disablePadding: true, sx: { display: "block" } }, { children: _jsxs(ListItemButton, Object.assign({ sx: {
                                    minHeight: 48,
                                    justifyContent: open ? "initial" : "center",
                                    px: 2.5,
                                } }, { children: [_jsx(ListItemIcon, Object.assign({ sx: {
                                            minWidth: 0,
                                            mr: open ? 3 : "auto",
                                            justifyContent: "center",
                                        } }, { children: sideBar.lower[text].icon })), _jsx(ListItemText, { primary: text === "Kijelentkezés" ? (_jsx(LogoutButton, {})) : (_jsx(Link, Object.assign({ to: sideBar.lower[text].href }, { children: text }))), sx: { color: "gray", opacity: open ? 1 : 0 } })] })) }), text))) })] }))] })));
}
