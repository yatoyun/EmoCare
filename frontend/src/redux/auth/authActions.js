// authActions.js
import api from '../../api/api';
import { LOGIN_SUCCESS, LOGIN_FAIL, LOGOUT, REGISTER_SUCCESS, REGISTER_FAIL } from './authTypes';

export const loginUser = (username, password) => async (dispatch) => {
    try {
        const response = await api.post(`token/`, {
            username,
            password
        });
        if (response.status === 200) {
            dispatch({
                type: LOGIN_SUCCESS,
                payload: response.data
            });
        }
    } catch (error) {
        let errorMsg = 'Login failed due to server error';
        if (error.response) {
            if (error.response.status === 401) {
                errorMsg = 'Username or password is incorrect';
            } else if (error.response.data && error.response.data.detail) {
                errorMsg = error.response.data.detail;
            }
        }
        dispatch({
            type: LOGIN_FAIL,
            payload: errorMsg
        });
    }
};


export const logout = () => async (dispatch) => {
    try {
        await api.post('logout/');
        dispatch({ type: LOGOUT });
    } catch (error) {
        console.error('Logout error:', error);
    }
};

export const register = (username, password, token) => async dispatch => {
    try {
        // 登録処理
        await api.post('register/', { username, password, token });
        dispatch({ type: REGISTER_SUCCESS });
        console.log('Registered successfully');

        // 登録後の自動ログイン
        const loginResponse = await api.post('token/', { username, password });
        if (loginResponse.data && loginResponse.data.access) {
            // ログイン成功時の処理
            dispatch({ type: LOGIN_SUCCESS, payload: loginResponse.data });
            console.log('Logged in successfully');
        } else {
            dispatch({ type: LOGIN_FAIL });
        }
    } catch (error) {
        console.error('Registration failed:', error);
        dispatch({ type: REGISTER_FAIL });
    }
};