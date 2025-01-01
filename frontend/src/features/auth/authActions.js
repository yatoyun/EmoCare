import api from '../../configs/api'
import { loginSuccess, loginFail, logout, registerSuccess, registerFail } from './authSlice'

export const loginUser = (name, password) => async (dispatch) => {
  try {
    const response = await api.post('login/', { name, password })
    if (response.status === 200) {
      dispatch(loginSuccess(response.data))
      document.cookie = `sessionId=${response.data.access}; path=/; max-age=3600; SameSite=Strict`
    }
  } catch (error) {
    let errorMsg = 'Login failed due to server error'
    if (error.response) {
      if (error.response.status === 401) {
        errorMsg = 'Name or password is incorrect'
      } else if (error.response.data && error.response.data.detail) {
        errorMsg = error.response.data.detail
      }
    }
    dispatch(loginFail(errorMsg))
  }
}

export const logoutUser = () => async (dispatch) => {
  try {
    await api.post('logout/')
    dispatch(logout())
    document.cookie = 'sessionId=; path=/; expires=Thu, 01 Jan 1970 00:00:01 GMT;'
  } catch (error) {
    console.error('Logout error:', error)
  }
}

export const registerUser = (name, email, password) => async (dispatch) => {
  try {
    const loginResponse = await api.post('register/', { name, email, password })
    dispatch(registerSuccess())
    if (loginResponse.data && loginResponse.data.access) {
      dispatch(loginSuccess(loginResponse.data))
      document.cookie = `sessionId=${loginResponse.data.access}; path=/; max-age=3600; SameSite=Strict`
    }
  } catch (error) {
    console.error('Registration failed:', error)
    dispatch(registerFail(error.response?.data?.detail || 'Registration failed'))
  }
}

