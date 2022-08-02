import * as React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import DataUpload from "./views/DataUpload";
import AddConnection from "./views/AddConnection";
import HomePage from "./views/HomePage";
import Signup from "./views/SignupPage";
import PwdReset from "./views/PasswordReset";
import Login from "./views/LoginPage";
import Tables from "./views/Adatok";
import CssBaseline from "@mui/material/CssBaseline";
import NavBar from "./components/NavBar";
import AddTemplate from "./views/AddTemplate";
import ImportConfig from "./views/ImportConfig";
import AddSpecialQueries from "./views/AddSpecialQuery";
import Footer from "./components/Footer";

function App() {
	return (
		<React.Fragment>
			<CssBaseline enableColorScheme />
			<NavBar />
			<BrowserRouter>
				<Routes>
					<Route path='/adatok' element={<Tables />} />
					<Route path='/login' element={<Login />} />
					<Route path='/reset' element={<PwdReset />} />
					<Route path='/signup' element={<Signup />} />
					<Route path='/upload' element={<DataUpload />} />
					<Route
						path='/add-database-connections'
						element={<AddConnection />}
					/>
					<Route path='/' element={<HomePage />} />
					<Route path='/add-templates' element={<AddTemplate />} />
					<Route path='/import-config' element={<ImportConfig />} />
					<Route
						path='/add-special-queries'
						element={<AddSpecialQueries />}
					/>
				</Routes>
			</BrowserRouter>
			<Footer />
		</React.Fragment>
	);
}

export default App;
