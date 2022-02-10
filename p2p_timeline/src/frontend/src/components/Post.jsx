import React, { useEffect, useState } from 'react'
import logo from '../images/logo.svg'

export default function Post({ username, text, author, time }) {
  const [tweetTime, setTweetTime] = useState({ hour: '', date: '' })
  useEffect(() => {
    let date = new Date(time * 1000).toString().split(' ')
    setTweetTime({
      hour: date[4],
      date: `${date[1]} ${date[2]}`.replace('0', ''),
    })
  }, [time])

  return (
    <div className="bg-slate-50 dark:bg-inherit p-4 space-y-2">
      <div className="flex items-start justify-between">
        <div className="flex space-x-4">
          <img className="h-12 w-12 rounded-full bg-slate-800 border-2" src={logo} alt="profile" />
          <div>
            <p className="font-bold dark:text-white">
              {author.username || 'username'}
              <span className="font-light text-xs">&nbsp;({author.id})</span>
            </p>
            <p className="font-normal text-slate-600 dark:text-slate-300">{text}</p>
          </div>
        </div>
        <div className="flex items-end flex-col text-sm">
          <span className="text-slate-600 dark:text-slate-50 text-xs font-bold">{tweetTime.date}</span>
          <span className="text-slate-400 dark:text-slate-200 text-xs font-light">{tweetTime.hour}</span>
          <div className="flex space-x-2">
            {author.username === username ? <span className="text-teal-400 font-medium">My tweet</span> : null}
          </div>
        </div>
      </div>
    </div>
  )
}
