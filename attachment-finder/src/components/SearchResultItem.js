import _ from 'lodash'
import moment from 'moment'
import numeral from 'numeral'
import axios from 'axios'
import React from 'react'
import EventEmitterMixin from 'react-event-emitter-mixin'

import {getToken, GMAIL_API_ENDPOINT} from '../common_utils'

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

    return {
      id,
      payload,
      snippet,
      time: moment(parseInt(internalDate)).fromNow(),
      subject: _.find(payload.headers, {name: 'Subject'}).value,
      from: _.find(payload.headers, {name: 'From'}).value,
      to: _.find(payload.headers, {name: 'To'}).value
    }
  },

  downloadAttachment(part) {
    getToken()
    .then((token) => {
      return axios.get(`${GMAIL_API_ENDPOINT}/me/messages/${this.state.id}/attachments/${part.body.attachmentId}`, {
        params: {
          access_token: token
        }
      })
    })
    .then((res) => {
      // Gmail API returns broken(?) base64 string
      const data = res.data.data.replace(/-/g, '+').replace(/_/g, '/')
      const byteString = atob(data)
      const ab = new ArrayBuffer(byteString.length)
      const ia = new Uint8Array(ab)
      for(let i = 0; i < byteString.length; i++) {
        ia[i] = byteString.charCodeAt(i)
      }
      const blob = new Blob([ia], {type: part.mimeType})

      const tempLink = document.createElement('a')
      tempLink.href = window.URL.createObjectURL(blob)
      tempLink.setAttribute('download', part.filename)
      tempLink.click()
    })
    .catch(console.error)
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
            From : {this.state.from}<br />
            To : {this.state.to}<br />
            Date : {this.state.time}<br />
            Size : {numeral(part.body.size).format('0 b')}
          </div>
          <div className="mdl-card__actions mdl-card--border">
            <a className="mdl-button mdl-button--colored mdl-js-button mdl-js-ripple-effect"
               onClick={() => this.downloadAttachment(part)}>Download File</a>
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
