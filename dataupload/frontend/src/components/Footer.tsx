import Container from "@mui/material/Container";
import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import Link from "@mui/material/Link";
import React from "react";

export default function Footer() {
	return (
		<footer style={{ marginTop: 200 }}>
			<Box
				bgcolor='text.secondary'
				color='white'
				px={{ xs: 3, sm: 10 }}
				py={{ xs: 5, sm: 12 }}>
				<Container maxWidth='lg'>
					{/*1st column*/}
					<Grid container spacing={5}>
						<Grid item xs={12} sm={6} md={4} lg={3}>
							<Box borderBottom={1}>Help</Box>
							<Box>
								<Link href='/contact' color='inherit'>
									Contact
								</Link>
							</Box>
							<Box>
								<Link href='/about' color='inherit'>
									Support
								</Link>
							</Box>
							<Box>
								<Link href='/privacy' color='inherit'>
									Privacy Policy
								</Link>
							</Box>
						</Grid>
						{/* 2nd column */}
						<Grid item xs={12} sm={6} md={4} lg={3}>
							<Box borderBottom={1}>Account</Box>
							<Box>
								<Link href='/contact' color='inherit'>
									Login
								</Link>
							</Box>
							<Box>
								<Link href='/about' color='inherit'>
									Registration
								</Link>
							</Box>
						</Grid>
						{/* 3rd column */}
						<Grid item xs={12} sm={6} md={4} lg={3}>
							<Box borderBottom={1}>Messages</Box>
							<Box>
								<Link href='/contact' color='inherit'>
									Backup
								</Link>
							</Box>
							<Box>
								<Link href='/about' color='inherit'>
									History
								</Link>
							</Box>
							<Box>
								<Link href='/privacy' color='inherit'>
									Roll
								</Link>
							</Box>
						</Grid>
					</Grid>
					<Box
						textAlign='center'
						pt={{ xs: 5, sm: 10 }}
						pb={{ xs: 5, sm: 10 }}>
						dataupload &reg; {new Date().getFullYear()}
					</Box>
				</Container>
			</Box>
		</footer>
	);
}
