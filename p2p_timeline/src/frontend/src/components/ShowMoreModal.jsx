import logo from '../images/logo.svg'
import { Fragment, useState } from 'react'
import { Dialog, Transition } from '@headlessui/react'
import { UserAddIcon, UserRemoveIcon, XIcon } from '@heroicons/react/outline'

export default function ShowMoreModal({ users = [], handler, subscribe = undefined, text = '' }) {
  let [isOpen, setIsOpen] = useState(false)

  function closeModal() {
    setIsOpen(false)
  }

  function openModal() {
    setIsOpen(true)
  }

  return (
    <div className="group">
      <button
        type="button"
        onClick={openModal}
        className="text-sm w-full p-2 rounded-b-xl hover:opacity-50 duration-200"
      >
        <span>Show more {text.toLowerCase()}</span>
      </button>

      <Transition appear show={isOpen} as={Fragment}>
        <Dialog as="div" className="fixed inset-0 z-10 overflow-y-auto" onClose={closeModal}>
          <div className="min-h-screen px-4 text-center bg-black/50">
            <Transition.Child
              as={Fragment}
              enter="ease-out duration-300"
              enterFrom="opacity-0"
              enterTo="opacity-100"
              leave="ease-in duration-200"
              leaveFrom="opacity-100"
              leaveTo="opacity-0"
            >
              <Dialog.Overlay className="fixed inset-0" />
            </Transition.Child>

            {/* This element is to trick the browser into centering the modal contents. */}
            <span className="inline-block h-screen align-middle" aria-hidden="true">
              &#8203;
            </span>
            <Transition.Child
              as={Fragment}
              enter="ease-out duration-300"
              enterFrom="opacity-0 scale-95"
              enterTo="opacity-100 scale-100"
              leave="ease-in duration-200"
              leaveFrom="opacity-100 scale-100"
              leaveTo="opacity-0 scale-95"
            >
              <div className="inline-block w-full max-w-xl p-6 my-8 overflow-hidden text-left align-middle transition-all transform bg-slate-50 dark:bg-slate-700 shadow-xl rounded-2xl">
                <div className="flex items-center justify-between">
                  <Dialog.Title as="h3" className="text-lg font-medium leading-6 text-slate-800 dark:text-white">
                    {subscribe ? `Who To Follow` : subscribe === undefined ? `Followers` : `Following`}
                  </Dialog.Title>
                  <button
                    type="button"
                    className="inline-flex justify-center p-2 text-sm font-medium text-slate-800 bg-slate-100 border border-transparent rounded-md hover:bg-slate-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-slate-500"
                    onClick={closeModal}
                  >
                    <XIcon className="h-6 w-6" />
                  </button>
                </div>
                <ul className="p-3 space-y-4">
                  {users.map((user, index) => (
                    <li className="flex items-center justify-between" key={`follow-user-${index}`}>
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
                          onClick={(e) => handler(e, user)}
                          className={`flex ${
                            subscribe ? `bg-blue-500 dark:bg-blue-400` : `bg-rose-700 dark:bg-rose-600`
                          } duration-150 text-white dark:text-white hover:opacity-75
                            font-medium px-4 py-2 rounded-full self-end`}
                        >
                          {subscribe ? (
                            <>
                              <UserAddIcon className="h-6 w-5 mr-1" />
                              Follow
                            </>
                          ) : (
                            <>
                              <UserRemoveIcon className="h-6 w-5 mr-1" />
                              Unfollow
                            </>
                          )}
                        </button>
                      </div>
                    </li>
                  ))}
                </ul>
              </div>
            </Transition.Child>
          </div>
        </Dialog>
      </Transition>
    </div>
  )
}
