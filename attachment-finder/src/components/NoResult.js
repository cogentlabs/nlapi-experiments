import _ from 'lodash'
import React from 'react'

const style = {
  root: {
    marginTop: 20
  },

  card: {
    display: 'flex',
    color: '#E91E63',
    margin: '0px 40px 30px 40px',
    padding: 20,
    fontWeight: 'bold'
  }
}

module.exports = React.createClass({
  render() {
    return <div style={style.root}>
      <div style={style.card}>
        No Attachment Found :(
      </div>
    </div>
  }
})
