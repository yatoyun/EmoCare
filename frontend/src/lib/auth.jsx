import { configureAuth } from "react-query-auth";
import { Navigate, useLocation } from "react-router-dom";
import { z } from "zod";
import PropTypes from "prop-types";

import { paths } from "@/configs/paths";
import { Spinner } from "@/components/spinner";

import api from "./api";

const getUser = async () => {
	const response = await api.get("user/");

	return response.user;
};

const logout = () => {
	return api.post("logout/");
};

export const loginInputSchema = z.object({
	name: z.string().min(1, "Required"),
	password: z.string().min(4, "Required"),
});

const loginWithEmailAndPassword = (data) => {
	const validatedData = loginInputSchema.parse(data);
	return api.post("login/", validatedData);
};

export const registerInputSchema = z.object({
	name: z.string().min(1, "Required"),
	email: z.string().min(1, "Required"),
	password: z.string().min(4, "Required"),
});

const registerWithEmailAndPassword = (data) => {
	const validatedData = registerInputSchema.parse(data);
	return api.post("register/", validatedData);
};

const authConfig = {
	userFn: getUser,
	loginFn: async (data) => {
		await loginWithEmailAndPassword(data);

		// ユーザー情報を明示的に取得して更新
		const userResponse = await getUser();
		return userResponse;
	},
	registerFn: async (data) => {
		await registerWithEmailAndPassword(data);

		// ユーザー情報を明示的に取得して更新
		const userResponse = await getUser();
		return userResponse;
	},
	logoutFn: logout,
};

export const { useUser, useLogin, useLogout, useRegister } =
	configureAuth(authConfig);

export const ProtectedRoute = ({ children }) => {
	const { data: user, isLoading } = useUser();
	const location = useLocation();

	if (isLoading) {
		return (
			<div className="flex items-center justify-center h-screen">
				<Spinner />
			</div>
		);
	}

	if (!user) {
		const loginPath = paths.login.getHref(location.pathname);
		return <Navigate to={loginPath} replace />;
	}

	return children;
};

ProtectedRoute.propTypes = {
	children: PropTypes.node.isRequired,
};
