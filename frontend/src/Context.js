import { createContext } from 'react'
import axios from 'axios'

const context = createContext({
    backend: axios.create({
        baseURL: 'http://localhost:5000'
    })
})

export default context