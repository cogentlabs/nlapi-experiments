import React from 'react'
import {getToken} from '../common_utils'

module.exports = React.createClass({
  openPermissionRequester() {
    navigator.webkitGetUserMedia({video: false, audio: true}, (stream) => {}, console.log)

    chrome.windows.create({
      url: 'permission_requester.html',
      focused: true,
      type: 'popup',
      height: 400,
      width: 400
    })
  },

  componentDidMount(foo) {
    getToken(false)
    .then((token) => {
      console.log(`Token : ${token}`)
    })
    .catch(() => {  // not logging in
      getToken(true)
    })
    // this.openPermissionRequester()
  },

  render() {
    return <div />
  }
})
