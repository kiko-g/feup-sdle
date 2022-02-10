import React, { useEffect, useState } from 'react'
import logo from '../images/logo.svg'
import { UserAddIcon, UserRemoveIcon, RefreshIcon } from '@heroicons/react/outline'
import { localHeaders, contentHeader } from '../utils'
import ShowMoreModal from './ShowMoreModal'

const SET_TIMEOUT = process.env.REACT_APP_SET_TIMEOUT || 5000

export default function Sidebar({ user, setUser, classnames }) {
  const [toFollow, setToFollow] = useState([])
  const [followers, setFollowers] = useState([])
  const [following, setFollowing] = useState([])

  const fetchEntities = (url) => {
    const compareUsers = (x, y, key = 'identifier') => {
      const a = x[key]
      const b = y[key]

      if (a < b) return -1
      else if (a > b) return 1
      else return 0
    }

    fetch(`${url}/entities`, {
      method: 'GET',
      headers: localHeaders,
    })
      .then((response) => response.json())
      .then((response) => {
        console.log(response)
        setFollowers(
          response[0].sort((x, y) => {
            return compareUsers(x, y)
          })
        )
        setFollowing(
          response[1].sort((x, y) => {
            return compareUsers(x, y)
          })
        )
        setToFollow(
          response[2].sort((x, y) => {
            return compareUsers(x, y)
          })
        )
      })
      .catch((error) => console.error(error))
  }

  useEffect(() => {
    setTimeout(() => fetchEntities(user.url), SET_TIMEOUT)
  }, [user.url])

  const handleSubscribe = (event, userBackend) => {
    event.preventDefault()
    fetch(`${user.url}/subscribe`, {
      method: 'POST',
      headers: contentHeader,
      body: JSON.stringify(userBackend),
    })
      .then((response) => {
        console.log(response)
        if (!response.ok) {
          console.error('Response not ok')
          return
        }
        fetchEntities(user.url)
      })
      .catch((error) => console.error(error))
  }

  const handleUnsubscribe = (event, userBackend) => {
    event.preventDefault()
    fetch(`${user.url}/unsubscribe`, {
      method: 'POST',
      headers: contentHeader,
      body: JSON.stringify(userBackend),
    })
      .then((response) => {
        console.log(response)
        if (!response.ok) {
          console.error('Response not ok')
          return
        }
        fetchEntities(user.url)
      })
      .catch((error) => console.error(error))
  }

  const Followers = () => (
    <div className="overflow-y-hidden bg-slate-50 dark:bg-slate-700 shadow rounded-xl divide-y">
      <header className="flex items-center justify-between px-3 py-2 ">
        <span className="font-bold">Followers</span>
        <button
          type="button"
          onClick={() => fetchEntities(user.url)}
          className="flex items-center justify-center p-1 font-semibold rounded-full self-end
          bg-slate-400 text-white hover:opacity-80 duration-150"
        >
          <RefreshIcon className="h-4 w-4" />
        </button>
      </header>
      <ul className="text-sm p-3 space-y-2">
        {followers.length === 0 ? (
          <div className="flex items-center justify-center">
            <p className="font-normal text-rose-600 dark:text-rose-200">No one follows you yet.</p>
          </div>
        ) : (
          followers
            .filter((user, index) => index < 3)
            .map((user, index) => (
              <li className="flex items-center justify-start" key={`follower-user-${user.identifier}`}>
                <div className="flex space-x-4">
                  <img className="h-12 w-12 rounded-full bg-slate-800 border-2" src={logo} alt="profile" />
                  <div>
                    <p className="font-bold dark:text-white">
                      {user.username || 'username'}
                      <span className="font-light text-xs">&nbsp;({user.identifier})</span>
                    </p>
                    <p className="text-sm borderfont-normal text-slate-600 dark:text-slate-300">{`${user.host_ip}:${user.data_port}`}</p>
                  </div>
                </div>
              </li>
            ))
        )}
      </ul>
      <ShowMoreModal users={followers} handler={handleSubscribe} subscribe={undefined} />
    </div>
  )

  const Following = () => (
    <div className="bg-slate-50 dark:bg-slate-700 shadow rounded-xl divide-y">
      <header className="flex items-center justify-between px-3 py-2 ">
        <span className="font-bold">Following</span>
        <button
          type="button"
          onClick={() => fetchEntities(user.url)}
          className="flex items-center justify-center p-1 font-semibold rounded-full self-end
          bg-slate-400 text-white hover:opacity-80 duration-150"
        >
          <RefreshIcon className="h-4 w-4" />
        </button>
      </header>
      <ul className="text-sm p-3 space-y-2">
        {following.length === 0 ? (
          <div className="flex items-center justify-center">
            <p className="font-normal text-rose-600 dark:text-rose-200">You are not following anyone yet.</p>
          </div>
        ) : (
          following
            .filter((user, index) => index < 3)
            .map((user, index) => (
              <li className="flex items-center justify-between" key={`following-user-${user.identifier}`}>
                <div className="flex space-x-4">
                  <img className="h-12 w-12 rounded-full bg-slate-800 border-2" src={logo} alt="profile" />
                  <div>
                    <p className="font-bold dark:text-white">
                      {user.username || 'username'}
                      <span className="font-light text-xs">&nbsp;({user.identifier})</span>
                    </p>
                    <p className="text-sm borderfont-normal text-slate-600 dark:text-slate-300">{`${user.host_ip}:${user.data_port}`}</p>
                  </div>
                </div>
                <div className="flex">
                  <button
                    type="button"
                    onClick={(e) => handleUnsubscribe(e, user)}
                    className="flex bg-rose-700 text-white dark:bg-rose-600 dark:text-white hover:opacity-75
                      duration-150 font-semibold px-4 py-2 rounded-full self-end"
                  >
                    <UserRemoveIcon className="h-6 w-5 mr-1" />
                    Unfollow
                  </button>
                </div>
              </li>
            ))
        )}
      </ul>
      <ShowMoreModal users={following} handler={handleSubscribe} subscribe={false} />
    </div>
  )

  const WhoToFollow = () => (
    <div className="bg-slate-50 dark:bg-slate-700 shadow rounded-xl divide-y">
      <header className="flex items-center justify-between px-3 py-2 ">
        <span className="font-bold">Who to follow</span>
        <button
          type="button"
          onClick={() => fetchEntities(user.url)}
          className="flex items-center justify-center p-1 font-semibold rounded-full self-end
          bg-slate-400 text-white hover:opacity-80 duration-150"
        >
          <RefreshIcon className="h-4 w-4" />
        </button>
      </header>
      <ul className="text-sm p-3 space-y-2">
        {toFollow.length === 0 ? (
          <div className="flex items-center justify-center">
            <p className="font-normal text-rose-600 dark:text-rose-200">No users available to follow</p>
          </div>
        ) : (
          toFollow
            .filter((user, index) => index < 3)
            .map((user, index) => (
              <li className="flex items-center justify-between" key={`tofollow-user-${user.identifier}`}>
                <div className="flex space-x-4">
                  <img className="h-12 w-12 rounded-full bg-slate-800 border-2" src={logo} alt="profile" />
                  <div>
                    <p className="font-bold dark:text-white">
                      {user.username || 'username'}
                      <span className="font-light text-xs">&nbsp;({user.identifier})</span>
                    </p>
                    <p className="text-sm font-normal text-slate-600 dark:text-slate-300">{`${user.host_ip}:${user.data_port}`}</p>
                  </div>
                </div>
                <div className="flex">
                  <button
                    type="button"
                    className="flex bg-blue-500 text-white dark:bg-blue-400 dark:text-white hover:opacity-75
                      duration-150 font-semibold px-4 py-2 rounded-full self-end"
                    onClick={(e) => handleSubscribe(e, user)}
                  >
                    <UserAddIcon className="h-6 w-5 mr-1" />
                    Follow
                  </button>
                </div>
              </li>
            ))
        )}
      </ul>
      <ShowMoreModal users={toFollow} handler={handleSubscribe} subscribe={true} />
    </div>
  )

  return (
    <div className={`overflow-y-auto h-screen px-6 py-6 space-y-4 border-r ${classnames}`}>
      <Followers />
      <Following />
      <WhoToFollow />
    </div>
  )
}
