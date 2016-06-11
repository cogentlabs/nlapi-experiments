import React from 'react'
import EventEmitterMixin from 'react-event-emitter-mixin'

const RECOGNITION_STARTED = 'Listening...'
const RECOGNITION_FAILED = 'Failed. Retrying now'
const RECOGNITION_FINISHED = 'Recognized'

const style = {
  root: {
    width: 800,
    padding: '30px 0',
    color: '#ffffff',
    backgroundColor: '#4185ff',
    fontWeight: 'bold',
    display: 'flex'
  },

  textBox: {
    fontSize: 28,
    fontWeight: 500,
    lineHeight: 1.25,
    flex: 1,
    marginTop: 5
  },

  imageBox: {
    width: 170
  },

  wave: {
    height: 43,
    marginLeft: 42,
    marginRight: 42,
  },

  loadingBox: {
    marginTop: 3,
    marginRight: 42
  },

  loadingIcon: {
    width: 38,
    height: 38,
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
      text: null,
      isLoading: false
    }
  },

  componentWillMount() {
    this.eventEmitter('on', 'searchingFinished', () => {
      this.setState({isLoading: false})
    })

    this.eventEmitter('on', 'recognitionFinished', () => {
      this.setState({isLoading: true})
    })
  },

  componentDidMount() {
    this.recognition = this.initRecognition()
    this.recognition.start()
    // this.eventEmitter('emit', 'recognitionFinished', 'document sent to ray three weeks ago') // dummy
  },

  render() {
    const displayText = this.state.text || this.state.recognitionState
    const loadingIcon = this.state.isLoading
      ? <object data='images/loading.svg' type="image/svg+xml"></object>
      : null

    return (
      <div style={style.root}>
        <div style={style.imageBox}>
          <img style={style.wave} src='images/0_speech.png' />
        </div>
        <div style={style.textBox}>{displayText}</div>
        <div style={style.loadingBox}>{loadingIcon}</div>
      </div>
    )
  }
})
