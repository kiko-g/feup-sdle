import logo from '../images/logo.svg'
import React, { useState, useEffect, useMemo } from 'react'
import { LockClosedIcon, CheckIcon } from '@heroicons/react/solid'
import DarkModeSwitch from '../layout/DarkModeSwitch'
import { localHeaders, resolveAddress } from '../utils'

export default function Auth({ setUser }) {
  const [warning, setWarning] = useState(false)
  const [authType, setAuthType] = useState(false) // false is login, true is register
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const invalid = useMemo(() => username === '' || password === '', [username, password])

  const login = () => {
    const params = {
      method: 'POST',
      body: JSON.stringify({ username: username, password: password }),
      headers: localHeaders,
    }

    fetch('/login', params)
      .then((response) =>
        response.json().then((data) => {
          console.log(data)
          if (data.success === true) {
            // FIXME: somehow lift port correspondent to user.url
            setUser({ id: data.user.id, name: data.user.username, url: resolveAddress(data.user.id) })
          }
        })
      )
      .catch((err) => console.error(err))
  }

  const register = () => {
    const params = {
      method: 'POST',
      body: JSON.stringify({ username: username, password: password }),
      headers: localHeaders,
    }

    fetch('/register', params)
      .then((response) =>
        response.json().then((data) => {
          console.log(data)
          if (data.success === true) {
            // FIXME: somehow lift port correspondent to user.url
            setUser({ id: data.user.id, name: data.user.username, url: resolveAddress(data.user.id) })
          }
        })
      )
      .catch((err) => console.error(err))
  }

  const handleSubmit = (event) => {
    event.preventDefault()

    if (authType) register()
    else login()
  }

  useEffect(() => {
    //fetch stuff when mounted
  }, [])

  return (
    <>
      <div className="z-50 absolute top-4 right-4">
        <DarkModeSwitch />
      </div>
      <div className="relative min-h-full flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-md w-full space-y-8">
          <nav>
            <img className="mx-auto h-20 w-20 border-2 rounded-full bg-sky-900" src={logo} alt="icon" />
            {authType ? (
              <div>
                <h2 className="mt-6 text-center text-3xl font-extrabold text-slate-800 dark:text-sky-50">
                  Create an account
                </h2>
                <p className="mt-2 text-center text-sm text-slate-600 dark:text-sky-50">
                  Already have an account?{' '}
                  <button
                    onClick={() => setAuthType(false)}
                    className="font-medium text-sky-600 hover:text-sky-500 dark:text-sky-300 hover:dark:text-sky-400"
                  >
                    Login here
                  </button>
                </p>
              </div>
            ) : (
              <div>
                <h2 className="mt-6 text-center text-3xl font-extrabold text-slate-800 dark:text-sky-50">
                  Sign in to your account
                </h2>
                <p className="mt-2 text-center text-sm text-slate-600 dark:text-sky-50">
                  Or{' '}
                  <button
                    onClick={() => setAuthType(true)}
                    className="font-medium text-sky-600 hover:text-sky-500 dark:text-sky-300 hover:dark:text-sky-400"
                  >
                    register on the platform
                  </button>
                </p>
              </div>
            )}
          </nav>
          <form onSubmit={(e) => handleSubmit(e)} className="mt-8 space-y-6" method="POST">
            <input type="hidden" name="remember" defaultValue="true" />
            <div className="rounded-md shadow-sm -space-y-px">
              <div>
                <label htmlFor="username" className="sr-only">
                  Email address
                </label>
                <input
                  required
                  id="username"
                  type="text"
                  name="username"
                  autoComplete="off" //https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/autocomplete
                  placeholder="Username"
                  value={username}
                  onChange={(e) => {
                    setUsername(e.target.value)
                  }}
                  className="appearance-none rounded-none relative block w-full px-3 py-2 border border-slate-300 placeholder-slate-500 text-slate-900 rounded-t-md focus:outline-none focus:ring-sky-500 focus:border-sky-500 focus:z-10 sm:text-sm"
                />
              </div>
              <div>
                <label htmlFor="password" className="sr-only">
                  Password
                </label>
                <input
                  required
                  id="password"
                  name="password"
                  type="password"
                  autoComplete="off"
                  placeholder="Password"
                  value={password}
                  onChange={(e) => {
                    setPassword(e.target.value)
                  }}
                  className="appearance-none rounded-none relative block w-full px-3 py-2 border border-slate-300 placeholder-slate-500 text-slate-900 rounded-b-md focus:outline-none focus:ring-sky-500 focus:border-sky-500 focus:z-10 sm:text-sm"
                />
              </div>
            </div>

            <div>
              <button
                type="submit"
                onMouseOver={() => {
                  if (invalid) setWarning(true)
                }}
                onMouseLeave={() => {
                  setWarning(false)
                }}
                disabled={invalid ? true : false}
                className={`group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-sky-600 ${
                  invalid ? `cursor-not-allowed` : `hover:bg-sky-700`
                } focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-sky-500`}
              >
                {invalid ? (
                  <span className="absolute left-0 inset-y-0 flex items-center pl-3">
                    <LockClosedIcon className="h-5 w-5 text-slate-800 group-hover:text-slate-800" aria-hidden="true" />
                  </span>
                ) : (
                  <span className="absolute left-0 inset-y-0 flex items-center pl-3">
                    <CheckIcon className="h-5 w-5 text-teal-300 group-hover:text-teal-400" aria-hidden="true" />
                  </span>
                )}
                Sign in
              </button>
              {warning ? (
                <p className="text-center text-sm text-rose-400">Username and password can't be empty.</p>
              ) : null}
            </div>
          </form>
        </div>
      </div>
    </>
  )
}
