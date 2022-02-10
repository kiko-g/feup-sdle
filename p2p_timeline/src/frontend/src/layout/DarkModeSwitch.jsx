import useDarkMode from '../hooks/useDarkMode'
import { Switch } from '@headlessui/react'
import { MoonIcon, SunIcon } from '@heroicons/react/solid'

export default function DarkModeSwitch() {
  const [darkTheme, setDarkTheme] = useDarkMode()
  const handleMode = () => setDarkTheme(!darkTheme)

  return (
    <Switch.Group>
      <div className="flex items-center">
        <Switch.Label passive className="mr-2">
          {darkTheme ? (
            <MoonIcon className="block h-6 w-6 transition duration-200 ease text-slate-400" aria-hidden="true" />
          ) : (
            <SunIcon className="block h-6 w-6 transition duration-200 ease text-orange-300" aria-hidden="true" />
          )}
        </Switch.Label>
        <Switch
          checked={darkTheme}
          onChange={handleMode}
          className={`${
            darkTheme ? 'bg-blue-300' : 'bg-slate-400'
          } relative inline-flex items-center h-6 rounded-full w-11 transition-colors focus:outline-none`}
        >
          <span
            className={`${
              darkTheme ? 'translate-x-6' : 'translate-x-1'
            } inline-block w-4 h-4 transform bg-white rounded-full transition-transform`}
          />
        </Switch>
      </div>
    </Switch.Group>
  )
}
