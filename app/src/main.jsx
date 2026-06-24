import './index.css'
import React from 'react'
import ReactDOM from 'react-dom/client'
import { createRouter, RouterProvider, createHashHistory } from '@tanstack/react-router'
import { routeTree } from './routeTree.gen.js'

const hashHistory = createHashHistory()

const router = createRouter({
  routeTree,
  history: hashHistory,
})

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
)