import { jsx as _jsx } from "react/jsx-runtime";
import Userfront from "@userfront/react";
import { Navigate } from "react-router-dom";
export default function HomePage() {
    if (!Userfront.accessToken())
        return _jsx(Navigate, { to: '/login' });
    return (_jsx("div", Object.assign({ className: 'flex justify-center items-center' }, { children: _jsx("h1", Object.assign({ className: 'text-tetriarydark' }, { children: "Home Page" })) })));
}
