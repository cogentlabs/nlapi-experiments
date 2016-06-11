import _ from 'lodash'
import axios from 'axios'
import React from 'react'
import EventEmitterMixin from 'react-event-emitter-mixin'
import SearchResultItem from './SearchResultItem'

import {getToken, GMAIL_API_ENDPOINT, QUERY_CONV_URL} from '../common_utils'
const GMAIL_MAX_RESULT = 100

const convertNL2Query = (text) => {
  return new Promise((resolve, reject) => {
    axios.get(QUERY_CONV_URL, {
      params: {q: text}
    })
    .then((res) => resolve(res.data))
    .catch((res) => reject(res.data))
  })
}

const gmailMessageList = (query) => {
  return new Promise((resolve, reject) => {
    getToken()
    .then((token) => {
      return axios.get(`${GMAIL_API_ENDPOINT}/me/messages`, {
        params: {
          q: '"has:attachment"',
          access_token: token,
          maxResults: GMAIL_MAX_RESULT
        }
      })
    })
    .then((res) => { resolve(res.data) })
    .catch(reject)
  })
}

const getMessage = (id) => {
  return new Promise((resolve, reject) => {
    getToken()
    .then((token) => {
      return axios.get(`${GMAIL_API_ENDPOINT}/me/messages/${id}`, {
        params: {
          access_token: token,
          maxResults: GMAIL_MAX_RESULT
        }
      })
    })
    .then((res) => { resolve(res.data) })
    .catch(reject)
  })
}

module.exports = React.createClass({
  mixins: [EventEmitterMixin],

  searchResultItems() {
    return this.state.messages.map((message) =>
      <SearchResultItem key={message.id} message={message} />
    )
  },

  getInitialState() {
    return {
      messages: []
    }
  },

  componentWillMount() {
    this.eventEmitter('on', 'recognitionFinished', (text) => {
      // convertNL2Query(text)
      // .then((query) => {
      //   console.log(query)
      // })
      // .catch(console.error)

      gmailMessageList()
      .then((messageList) => {
        const messagePromises = messageList.messages.map((message) => getMessage(message.id))
        Promise.all(messagePromises).then((messages) => { this.setState({messages}) })
      })
      .catch(console.error)
    })
  },

  render() {
    return <div>
      {this.searchResultItems()}
    </div>
  }
})
