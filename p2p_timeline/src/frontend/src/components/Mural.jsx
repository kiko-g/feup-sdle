import React, { useEffect, useState } from 'react'
import Post from '../components/Post'
import Compose from './Compose'
import DarkModeSwitch from '../layout/DarkModeSwitch'
import { localHeaders } from '../utils'
import Footer from './Footer'

const REFRESH_RATE = process.env.REACT_APP_TIMELINE_RATE || 5000

export default function Mural({ user, setUser, classnames }) {
  const [tweets, setTweets] = useState([])

  const fetchTimeline = (url) => {
    const compareTweets = (x, y, key = 'post_time') => {
      const a = x[key]
      const b = y[key]

      if (a > b) return -1
      else if (a < b) return 1
      else return 0
    }

    fetch(`${url}/timeline`, {
      method: 'GET',
      headers: localHeaders,
    })
      .then((response) => response.json())
      .then((response) => {
        const tweetsList = []
        response.map((elem) => tweetsList.push(...elem.list_tweets))
        tweetsList.sort((x, y) => {
          return compareTweets(x, y)
        })
        setTweets(tweetsList)
      })
  }

  useEffect(() => {
    setInterval(() => fetchTimeline(user.url), REFRESH_RATE)
  }, [user.url])

  return (
    <div className={`overflow-y-auto h-screen relative border-x ${classnames}`}>
      <div className="bg-slate-100 dark:bg-slate-800 shadow flex items-center justify-between p-4">
        <p className="font-normal">
          <span className="font-bold">Timeline</span>&nbsp;&middot;&nbsp;Home
        </p>
        <DarkModeSwitch />
      </div>
      <Compose user={user} setUser={setUser} />
      <div className="divide-y">
        {tweets.length === 0 ? (
          <div className="flex items-center justify-center py-2">
            <p>No tweets found yet.</p>
          </div>
        ) : (
          tweets.map((tweet, index) => (
            <Post
              username={user.username}
              author={{ id: tweet.author_id, username: tweet.author_username || `username` }}
              text={tweet.text}
              time={tweet.post_time}
              key={`tweet-${index}`}
            />
          ))
        )}
        <Footer />
      </div>
    </div>
  )
}
