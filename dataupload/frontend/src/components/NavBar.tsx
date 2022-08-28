import DownloadingIcon from "@mui/icons-material/Downloading";
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
import InboxIcon from "@mui/icons-material/MoveToInbox";
import MailIcon from "@mui/icons-material/Mail";
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

const DrawerHeader = styled("div")(({ theme }) => ({
	display: "flex",
	alignItems: "center",
	justifyContent: "flex-end",
	padding: theme.spacing(0, 1),
	// necessary for content to be below app bar
	...theme.mixins.toolbar,
}));

const AppBar = styled(MuiAppBar, {
	shouldForwardProp: (prop) => prop !== "open",
})(({ theme, open }) => ({
	zIndex: theme.zIndex.drawer + 1,
	transition: theme.transitions.create(["width", "margin"], {
		easing: theme.transitions.easing.sharp,
		duration: theme.transitions.duration.leavingScreen,
	}),
	...(open && {
		marginLeft: drawerWidth,
		width: `calc(100% - ${drawerWidth}px)`,
		transition: theme.transitions.create(["width", "margin"], {
			easing: theme.transitions.easing.sharp,
			duration: theme.transitions.duration.enteringScreen,
		}),
	}),
}));

const Drawer = styled(MuiDrawer, { shouldForwardProp: (prop) => prop !== "open" })(({ theme, open }) => ({
	width: drawerWidth,
	flexShrink: 0,
	whiteSpace: "nowrap",
	boxSizing: "border-box",
	...(open && {
		...openedMixin(theme),
		"& .MuiDrawer-paper": openedMixin(theme),
	}),
	...(!open && {
		...closedMixin(theme),
		"& .MuiDrawer-paper": closedMixin(theme),
	}),
}));

export default function MiniDrawer() {
	const sideBar = ["dark-frost-2k269", "winter-salad-brlnr", "ancient-river-26kn4"].includes(Userfront.user.username)
		? {
				upper: {
					"Upload": { href: "/upload/", icon: <UploadFileIcon /> },
					"Feltöltések": { href: "/uploads", icon: <DownloadingIcon /> },
					"Adatok": { href: "/adatok/", icon: <StorageIcon /> },
					"Import Konfig": { href: "/import-config/", icon: <ImportExportIcon /> },
					"Tábla Létrehozása": { href: "/create-table/", icon: <TableViewIcon /> },
					"Felhasználó Hozzáadása": { href: "/signup/", icon: <AssignmentIndIcon /> },
				},
				lower: {
					Fiók: { href: "/upload", icon: <AccountCircleSharpIcon /> },
					Kijelentkezés: {
						href: "/login",
						icon: (
							<LogoutIcon
								onClick={(event) => {
									event.preventDefault();
									Userfront.logout();
								}}
							/>
						),
					},
				},
		  }
		: Userfront.accessToken()
		? {
				upper: {
					Upload: { href: "/upload/", icon: <UploadFileIcon /> },
					Feltöltések: { href: "/uploads", icon: <DownloadingIcon /> },
					Adatok: { href: "/adatok/", icon: <StorageIcon /> },
				},
				lower: {
					Fiók: { href: "/upload", icon: <AccountCircleSharpIcon /> },
					Kijelentkezés: {
						href: "/login",
						icon: (
							<LogoutIcon
								onClick={(event) => {
									event.preventDefault();
									Userfront.logout();
								}}
							/>
						),
					},
				},
		  }
		: { upper: { Bejelentkezés: { href: "/login/", icon: <LoginIcon /> } }, lower: {} };
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

	return (
		<Box sx={{ display: "flex", marginBottom: 20 }}>
			<CssBaseline />
			<AppBar position='fixed' open={open} sx={{ backgroundColor: "#013970" }}>
				<Toolbar>
					<IconButton
						color='inherit'
						aria-label='open drawer'
						onClick={handleDrawerOpen}
						edge='start'
						sx={{
							marginRight: 5,
							...(open && { display: "none" }),
						}}>
						<MenuIcon />
					</IconButton>
					<Typography variant='h6' noWrap component='div'>
						Adatfeltöltés
					</Typography>
				</Toolbar>
			</AppBar>
			<Drawer variant='permanent' open={open} sx={{ marginLeft: 10 }}>
				<DrawerHeader>
					<IconButton onClick={handleDrawerClose}>
						{theme.direction === "rtl" ? <ChevronRightIcon /> : <ChevronLeftIcon />}
					</IconButton>
				</DrawerHeader>
				<Divider />
				<List>
					{Object.keys(sideBar.upper).map((text) => (
						<Link to={sideBar.upper[text].href}>
							<ListItem key={text} disablePadding sx={{ display: "block" }}>
								<ListItemButton
									sx={{
										minHeight: 48,
										justifyContent: open ? "initial" : "center",
										px: 2.5,
									}}>
									<ListItemIcon
										sx={{
											minWidth: 0,
											mr: open ? 3 : "auto",
											justifyContent: "center",
										}}>
										{sideBar.upper[text].icon}
									</ListItemIcon>
									<ListItemText primary={text} sx={{ color: "gray", opacity: open ? 1 : 0 }} />
								</ListItemButton>
							</ListItem>
						</Link>
					))}
				</List>
				<Divider />
				<List>
					{Object.keys(sideBar.lower).map((text) => (
						<ListItem key={text} disablePadding sx={{ display: "block" }}>
							<ListItemButton
								sx={{
									minHeight: 48,
									justifyContent: open ? "initial" : "center",
									px: 2.5,
								}}>
								<ListItemIcon
									sx={{
										minWidth: 0,
										mr: open ? 3 : "auto",
										justifyContent: "center",
									}}>
									{sideBar.lower[text].icon}
								</ListItemIcon>
								<ListItemText
									primary={
										text === "Kijelentkezés" ? (
											<LogoutButton />
										) : (
											<Link to={sideBar.lower[text].href}>{text}</Link>
										)
									}
									sx={{ color: "gray", opacity: open ? 1 : 0 }}
								/>
							</ListItemButton>
						</ListItem>
					))}
				</List>
			</Drawer>
		</Box>
	);
}
