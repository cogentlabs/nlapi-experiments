import React from 'react'
import EventEmitterMixin from 'react-event-emitter-mixin'

const style = {
  textInput: {
    color: '#333333',
    fontWeight: 'bold'
  }
}

module.exports = React.createClass({
  mixins: [EventEmitterMixin],

  initRecognition() {
    const recognition = new webkitSpeechRecognition()
    recognition.lang = 'en';
    console.log(recognition)

    recognition.addEventListener('result', (event) => {
      console.log(event.results)
      const text = event.results.item(0).item(0).transcript
      this.setState({text})

      if(event.results.item(0).isFinal) {
        this.eventEmitter('emit', 'recognitionFinished', text)
      }
    }, false)

    return recognition
  },

  startRecognition() {
    this.state.recognition.start()
  },

  getInitialState() {
    // navigator.getUserMedia({video: false, audio: true}, (stream) => {
    //   console.log("step2")
    // }, console.error)

    return {
      recognition: this.initRecognition(),
      text: null
    }
  },

  componentDidMount() {
    this.startRecognition()
    this.eventEmitter('emit', 'recognitionStarted')
  },


  render() {
    const displayText = this.state.text || 'Listening...'

    return (
      <p className="mdl-card__supporting-text">{displayText}</p>
    )
  }
})
