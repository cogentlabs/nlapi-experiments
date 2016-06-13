import React from 'react'
import EventEmitterMixin from 'react-event-emitter-mixin'
import {translate} from '../common_utils'

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
    cursor: 'pointer'
  },

  optionBox: {
    marginTop: 3,
    marginRight: 42
  },

  loadingIcon: {
    width: 38,
    height: 38,
  }
}

const labelDict = {
  en: {
    initializing: 'initializing...',
    listening: 'Listening...',
    failed: 'Failed. Trying again...'
  },
  ja: {
    initializing: '準備中です...',
    listening: 'お話ください',
    failed: '聞き取りに失敗しました'
  }
}


module.exports = React.createClass({
  mixins: [EventEmitterMixin],

  recognition: null,

  i18nLabel(type) {
    return labelDict[this.state.inputLanguage][type]
  },

  initRecognition() {
    const recognition = new webkitSpeechRecognition()
    recognition.lang = this.state.inputLanguage
    console.log(recognition)

    recognition.onnomatch = () => {
      this.setState({
        text: null,
        recognitionState: this.i18nLabel('failed')
      })
      this.state.recognition.start()
    }

    recognition.onstart = () => {
      this.setState({
        text: null,
        recognitionState: this.i18nLabel('listening')
      })
      this.eventEmitter('emit', 'recognitionInitiated', null)
    }

    recognition.onresult = (event) => {
      _.each(event.results, (result) => {
        console.log(result)
        const text = result[0].transcript

        this.setState({text, recognitionState: null})

        if(result.isFinal) {
          this.setState({
            text,
            recognitionState: null
          })

          if(_.isEqual(this.state.inputLanguage, 'en')) {
            this.eventEmitter('emit', 'recognitionFinished', text)
          }
          else {
            translate(this.state.inputLanguage, 'en', text)
            .then((translatedText) => {
              console.log(`Translated to : ${translatedText}`)
              this.eventEmitter('emit', 'recognitionFinished', translatedText)
            })
            .catch(console.error)
          }
        }
      })
    }

    return recognition
  },

  switchLanguage() {
    const newLang = _.isEqual(this.state.inputLanguage, 'en') ? 'ja' : 'en'
    this.setState({inputLanguage: newLang}, () => {
      this.startOver()
    })
  },

  startOver() {
    this.recognition.stop()
    this.recognition = this.initRecognition()
    this.recognition.start()
  },

  optionIcon() {
    if(this.state.isLoading) {
      return <object data='images/loading.svg' type="image/svg+xml"></object>
    }

    return <div style={{marginTop: 7}}>
      <img src='./images/language.png'
           onClick={this.switchLanguage}
           style={{cursor: 'pointer'}}
           width={30} />
    </div>

    return null
  },

  getInitialState() {
    return {
      recognitionState: labelDict.en.initializing,
      text: null,
      isLoading: false,
      inputLanguage: 'ja'
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
    const displayText = this.state.text || <span style={{color: '#eee'}}>{this.state.recognitionState}</span>

    return (
      <div style={style.root}>
        <div style={style.imageBox}>
          <img style={style.wave}
               onClick={this.startOver}
               src='images/0_speech.png' />
        </div>
        <div style={style.textBox}>{displayText}</div>
        <div style={style.optionBox}>{this.optionIcon()}</div>
      </div>
    )
  }
})
