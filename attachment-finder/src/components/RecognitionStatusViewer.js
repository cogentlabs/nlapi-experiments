import React from 'react'
import EventEmitterMixin from 'react-event-emitter-mixin'

const style = {
  textInput: {
    color: '#333333'
  }
}

module.exports = React.createClass({
  mixins: [EventEmitterMixin],

  render() {
    return <div />
  }
})
