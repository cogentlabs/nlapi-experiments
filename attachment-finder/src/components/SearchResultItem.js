import _ from 'lodash'
import moment from 'moment'
import numeral from 'numeral'
import axios from 'axios'
import React from 'react'
import EventEmitterMixin from 'react-event-emitter-mixin'

import {getToken, GMAIL_API_ENDPOINT, getIconByMimeType} from '../common_utils'

import SUPPORTED_MIME_TYPES from '../mime_filter'

const style = {
  card: {
    color: '#4a4a4a',
    backgroundColor: '#f5f5f5',
    marginLeft: 40,
    marginRight: 40,
    marginBottom: 30
  },

  filename: {
    color: '#4a4a4a',
    fontSize: 18,
    fontWeight: 500
  },

  metadata: {
    color: '#4a4a4a',
    fontSize: 14,
    whiteSpace: 'nowrap',
    overflow: 'hidden',
    textOverflow: 'ellipsis'
  }
}

module.exports = React.createClass({
  mixins: [EventEmitterMixin],

  propTypes: {
    message: React.PropTypes.object.isRequired,
  },

  getInitialState() {
    const {id, internalDate, payload, snippet} = this.props.message

    const toAddrs = _(payload.headers)
    .filter({name: 'To'})
    .map((item) => item.value)
    .value()

    return {
      id,
      payload,
      snippet,
      time: moment(parseInt(internalDate)).fromNow(),
      subject: _.find(payload.headers, {name: 'Subject'}).value,
      from: _.find(payload.headers, {name: 'From'}).value,
      to: toAddrs
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

      // Download the blog as a file
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
      const iconPath = `images/${getIconByMimeType(part.mimeType)}`

      return (
        <div key={part.body.attachmentId} style={style.card}>
          <img src={iconPath} />
          <div style={style.filename}>{part.filename}</div>
          <div>
            <div style={style.metadata}>From : {this.state.from}</div>
            <div style={style.metadata}>To : {this.state.to}</div>
            <div style={style.metadata}>Date : {this.state.time}</div>
            <div style={style.metadata}>Size : {numeral(part.body.size).format('0 b')}</div>
          </div>
          <div>
            <a onClick={() => this.downloadAttachment(part)}>Download File</a>
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
