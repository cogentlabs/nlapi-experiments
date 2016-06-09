'use strict'
import React from 'react'
import ReactDOM from 'react-dom'
import EventEmitterMixin from 'react-event-emitter-mixin'

// import Speech2Text from './components/Speech2Text'
import PermissionRequester from './components/PermissionRequester'
import Speech2Text from './components/Speech2Text'
import SearchResult from './components/SearchResult'

const style = {
  rootWrapper: {
    padding: 10,
    width: 340
  }
}

const App = React.createClass({
  mixins: [EventEmitterMixin],

  render() {
    return <div style={style.rootWrapper}>
      <PermissionRequester />
      <Speech2Text />
      <SearchResult />
    </div>
  }
})

ReactDOM.render(<App />,
  document.getElementById('content')
)
