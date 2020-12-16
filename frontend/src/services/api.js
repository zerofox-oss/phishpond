import axios from 'axios'
import Cookies from 'js-cookie'

export default axios.create({
  baseURL: '/api',
  timeout: 15000,

  headers: {
    'X-CSRFtoken': Cookies.get('csrftoken')
  }
})
