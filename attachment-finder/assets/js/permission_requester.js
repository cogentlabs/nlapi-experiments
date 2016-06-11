'use strict'

navigator.getUserMedia = navigator.webkitGetUserMedia

navigator.getUserMedia({video: false, audio: true}, (stream) => {
  window.close()
}, console.log)
