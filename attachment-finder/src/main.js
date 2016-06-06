import React from 'react'
import ReactDOM from 'react-dom'

const App = React.createClass({
  render() {
    return <div>hey dude</div>
  }
})

ReactDOM.render(<App />,
  document.getElementById('content')
)
