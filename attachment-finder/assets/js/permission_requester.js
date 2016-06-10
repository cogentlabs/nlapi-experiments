'use strict'

navigator.getUserMedia = navigator.webkitGetUserMedia

navigator.getUserMedia({video: false, audio: true}, (stream) => {
}, console.log)
