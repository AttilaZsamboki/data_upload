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
	return (
		<React.Fragment>
			<QueryClientProvider client={queryClient}>
				<CssBaseline enableColorScheme />
				<NavBar />
				<BrowserRouter>
					<Routes>
						<Route path='/adatok' element={<Adatok />} />
						<Route path='/login' element={<Login />} />
						<Route path='/reset' element={<PwdReset />} />
						<Route path='/signup' element={<Signup />} />
						<Route path='/upload' element={<DataUpload />} />
						<Route path='/' element={<HomePage />} />
						<Route path='/add-templates' element={<AddTemplate />} />
						<Route path='/import-config' element={<ImportConfig />} />
						<Route path='/add-special-queries' element={<AddSpecialQueries />} />
						<Route path='/create-table' element={<CreateTable />} />
					</Routes>
				</BrowserRouter>
				<Footer />
				<ReactQueryDevtools initialIsOpen={false} />
			</QueryClientProvider>
		</React.Fragment>
	);
}

export default App;
