import React from 'react'

module.exports = React.createClass({
  // 4/bs-vLRT9UWghxzsH7K6-q_Oh3faoIroOT9fluiGTU_M
  interactiveSignIn() {
    chrome.identity.getAuthToken({interactive: true}, (token) => {
      if (chrome.runtime.lastError) {
        console.error(chrome.runtime.lastError)
      } else {
        console.log(`Token acquired: ${token}`)
      }
    })
  },

  // revokeToken() {
  //   chrome.identity.getAuthToken({interactive: false }, (currentToken) => {
  //     // Removing local cache
  //     chrome.identity.removeCachedAuthToken({ token: current_token })
  //
  //     // Request server to revoke
  //     const xhr = new XMLHttpRequest();
  //     xhr.open('GET', `https://accounts.google.com/o/oauth2/revoke?token=${current_token}`)
  //     xhr.send();
  //   })
  // },

  componentDidMount(foo) {
    this.interactiveSignIn()

    // navigator.webkitGetUserMedia({video: false, audio: true}, (stream) => {
    // }, console.log)

    // chrome.windows.create({
    //   url : 'permission_requester.html',
    //   focused : true,
    //   type : 'popup',
    //   height : 400,
    //   width : 400
    // })
  },

  render() {
    return <div />
  }
})
