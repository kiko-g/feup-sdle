import React, { useState } from 'react'
import Layout from '../layout/Layout'
import Mural from '../components/Mural'
import Sidebar from '../components/Sidebar'
import Auth from '../components/Auth'

export default function Homepage() {
  const [user, setUser] = useState({ id: '', name: '', url: '' })

  return (
    <Layout>
      {user.name === '' ? (
        <Auth setUser={setUser} />
      ) : (
        <div className="grid grid-cols-1 xl:grid-cols-3">
          <Mural user={user} setUser={setUser} classnames={`xl:col-span-2`} />
          <Sidebar user={user} setUser={setUser} classnames={`hidden xl:block xl:col-span-1`} />
        </div>
      )}
    </Layout>
  )
}
