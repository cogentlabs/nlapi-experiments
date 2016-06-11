import React from 'react'
import EventEmitterMixin from 'react-event-emitter-mixin'

const RECOGNITION_STARTED = 'Listening'
const RECOGNITION_FAILED = 'Failed. Retrying now'
const RECOGNITION_FINISHED = 'Recognized'

const style = {
  root: {
    // height: 100,
    paddingTop: 31,
    color: '#ffffff',
    backgroundColor: '#4185ff',
    fontWeight: 'bold'
  },
  wave: {
    height: 43,
    marginLeft: 42,
    marginRight: 42,
  },
  text: {
    fontSize: 28,
    fontWeight: 500,
    lineHeight: 1.25
  }
}

module.exports = React.createClass({
  mixins: [EventEmitterMixin],

  recogniztion: null,

  initRecognition() {
    const recognition = new webkitSpeechRecognition()
    recognition.lang = 'en';
    console.log(recognition)

    recognition.onnomatch = () => {
      this.setState({
        text: null,
        recognitionState: RECOGNITION_FAILED
      })
      this.state.recognition.start()
    }

    recognition.onresult = (event) => {
      _.each(event.results, (result) => {
        console.log(result)
        const text = result[0].transcript
        if(result.isFinal) {
          this.setState({
            text,
            recognitionState: RECOGNITION_FINISHED
          })
          this.eventEmitter('emit', 'recognitionFinished', text)
        }
        else {
          this.setState({text})
        }
      })
    }

    return recognition
  },

  getInitialState() {
    return {
      recognitionState: RECOGNITION_STARTED,
      text: null
    }
  },

  componentDidMount() {
    this.recognition = this.initRecognition()
    // this.recognition.start()
    this.eventEmitter('emit', 'recognitionFinished', 'document sent to ray') // dummy
  },


  render() {
    const displayText = this.state.text || this.state.recognitionState

    return (
      <div style={style.root}>
        <img style={style.wave} src='images/0_speech.png' />
        <span style={style.text}>{displayText}</span>
      </div>
    )
  }
})
