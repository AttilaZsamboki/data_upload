import * as React from "react";
import Userfront from "@userfront/react";

export default function ProfileIcon() {
	return (
		<div>
			<img
				style={{ width: 30, height: 30, borderRadius: 9999999999, marginBottom: 10 }}
				src={Userfront.user.image || Userfront.user.data.profileImage}
			/>
		</div>
	);
}
