import _ from 'lodash'
import moment from 'moment'
import React from 'react'
import EventEmitterMixin from 'react-event-emitter-mixin'

import SUPPORTED_MIME_TYPES from '../mime_filter'

const style = {
  card: { marginBottom: 15 },
  title: {
    color: '#fff',
    background: '#1D7044'
  }
}

module.exports = React.createClass({
  mixins: [EventEmitterMixin],

  propTypes: {
    message: React.PropTypes.object.isRequired,
  },

  getInitialState() {
    const {id, internalDate, payload, snippet} = this.props.message
    const subject = _.find(payload.headers, {name: 'Subject'}).value

    return {
      id,
      timestamp: moment(parseInt(internalDate)).format('llll'),
      subject,
      payload,
      snippet
    }
  },

  buildCards() {
    const parts = this.state.payload.parts
    .filter((part) => _.includes(SUPPORTED_MIME_TYPES, part.mimeType))
    .filter((part) => _.has(part, 'body.attachmentId'))

    return parts.map((part) => {
      return (
        <div key={part.body.attachmentId} style={style.card} className="demo-card-square mdl-card mdl-shadow--2dp">
          <div style={style.title} className="mdl-card__title mdl-card--expand">
            <h2 className="mdl-card__title-text">{part.filename}</h2>
          </div>
          <div className="mdl-card__supporting-text">
            {this.state.timestamp}
          </div>
          <div className="mdl-card__actions mdl-card--border">
            <a className="mdl-button mdl-button--colored mdl-js-button mdl-js-ripple-effect">
              Open File
            </a>
          </div>
        </div>
      )
    })
  },

  render() {
    return <div>
      {this.buildCards()}
    </div>
  }
})
