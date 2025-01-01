import { createSlice } from '@reduxjs/toolkit'

const initialState = {
  isAuthenticated: false,
  user: null,
  error: null,
}

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    loginSuccess: (state, action) => {
      state.isAuthenticated = true
      state.user = action.payload
      state.error = null
    },
    loginFail: (state, action) => {
      state.isAuthenticated = false
      state.user = null
      state.error = action.payload
    },
    logout: (state) => {
      state.isAuthenticated = false
      state.user = null
      state.error = null
    },
    registerSuccess: (state) => {
      state.error = null
    },
    registerFail: (state, action) => {
      state.error = action.payload
    },
  },
})

export const { loginSuccess, loginFail, logout, registerSuccess, registerFail } = authSlice.actions

export default authSlice.reducer

