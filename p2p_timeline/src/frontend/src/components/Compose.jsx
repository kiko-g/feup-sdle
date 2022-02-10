import React, { useState } from 'react'
import logo from '../images/logo.svg'
import { PencilAltIcon } from '@heroicons/react/outline'
import { LogoutIcon } from '@heroicons/react/solid'
import { contentHeader } from '../utils'

export default function Compose({ user, setUser }) {
  const [input, setInput] = useState('')
  const handleSubmit = (event) => {
    event.preventDefault()
    fetch(`${user.url}/tweet`, {
      method: 'POST',
      headers: contentHeader,
      body: JSON.stringify({
        text: event.target.text.value,
      }),
    })
      .then(setInput(''))
      .catch((e) => console.log(e))
  }

  const handleLogout = (event) => {
    event.preventDefault()
    fetch(`${user.url}/logout`, {
      method: 'POST',
      headers: contentHeader,
    })
      .then((response) => {
        if (response.ok) setUser({ id: '', name: '', url: '' })
      })
      .catch((e) => console.log(e))
      .then((e) => (e.target.value = ''))
  }

  return (
    <form className="flex flex-col p-4 space-y-2 border-b" onSubmit={(e) => handleSubmit(e)}>
      <div className="flex items-start justify-between space-x-4">
        <img className="h-16 w-16 rounded-full bg-slate-800 border-2" src={logo} alt="profile" />
        <textarea
          id="text"
          type="text"
          name="text"
          rows={2}
          autoComplete="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          className="bg-slate-50 text-slate-700 dark:bg-slate-700 dark:text-white border-b
            p-3 text-lg w-full mx-2 shadow-sm rounded
            focus-visible:accent-slate-50"
          placeholder={`What's happening ${user.name}?`}
        />
      </div>
      <div className="flex items-center justify-between">
        <div className="text-sm font-normal ml-20">
          <p>
            Welcome, <span className="font-semibold">{user.name}</span>
          </p>
        </div>
        <div className="flex space-x-2 font-medium text-sm">
          <button
            type="button"
            onClick={(e) => handleLogout(e)}
            className="flex shadow bg-slate-600 text-white dark:bg-slate-500 dark:text-white hover:opacity-75 
            duration-150 px-3 py-1 rounded self-end"
          >
            <LogoutIcon className="h-[1.4rem] w-4 mr-1" />
            Logout
          </button>
          <button
            type="submit"
            className="flex shadow bg-teal-600 text-white dark:bg-teal-500 dark:text-white hover:opacity-75 
            duration-150 px-3 py-1 rounded self-end"
          >
            <PencilAltIcon className="h-[1.4rem] w-4 mr-1" />
            Post
          </button>
        </div>
      </div>
    </form>
  )
}
