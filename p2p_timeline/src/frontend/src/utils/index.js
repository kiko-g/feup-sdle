const API_URL = process.env.REACT_APP_API_URL
const API_PORT = process.env.REACT_APP_API_PORT

export const resolveAddress = (user_id = 0) => {
  return `${API_URL}:${parseInt(API_PORT) + parseInt(user_id)}`
}

export const localHeaders = {
  'Content-Type': 'application/json',
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Credentials': true,
}

export const contentHeader = {
  'Content-Type': 'application/json',
}

export const compareUsers = (x, y, key = 'identifier') => {
  const a = x[key]
  const b = y[key]

  if (a < b) return -1
  else if (a > b) return 1
  else return 0
}
