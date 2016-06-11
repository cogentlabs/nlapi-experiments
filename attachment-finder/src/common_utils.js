import _ from 'lodash'
import SUPPORTED_MIME_TYPES from './mime_filter'

const MIME_CATEGORIES = {
  document: [
    'application/msword'
  ],
  sheet: [
    'application/vnd.ms-excel',
    'application/msexcel',
    'application/x-msexcel'
  ],
  slide: [
    'application/pot',
    'application/pps',
    'application/ppt',
    'application/vnd.ms-powerpoint',
    'application/mspowerpoint'
  ],
  pdf: [
    'application/pdf'
  ],
  compressed: [
    'application/lha',
    'application/x-compress',
    'application/x-gzip',
    'application/x-excel',
    'application/x-gzip',
    'application/x-lha',
    'application/x-lha-compressed',
    'application/x-lk-rlestream',
    'application/x-lzh',
    'application/x-zip-compressed',
    'application/zip',
    'application/x-tar',
    'binary/lzh'
  ]
}

module.exports = {
  // QUERY_CONV_URL: 'http://gmail-query-builder.reactive.ai/',
  QUERY_CONV_URL: 'http://localhost:5000',
  GMAIL_API_ENDPOINT: 'https://www.googleapis.com/gmail/v1/users',

  getToken(interactive=false) {
    return new Promise((resolve, reject) => {
      chrome.identity.getAuthToken({interactive}, (token) => {
        if(chrome.runtime.lastError) {
          return reject(chrome.runtime.lastError)
        }
        resolve(token)
      })
    })
  },

  revokeToken() {
    chrome.identity.getAuthToken({interactive: false }, (currentToken) => {
      // Removing local cache
      chrome.identity.removeCachedAuthToken({ token: current_token })

      // Request server to revoke
      const xhr = new XMLHttpRequest()
      xhr.open('GET', `https://accounts.google.com/o/oauth2/revoke?token=${current_token}`)
      xhr.send()
    })
  },

  getIconByMimeType(mimeType) {
    if(_.includes(MIME_CATEGORIES.document, mimeType))   { return '1_document.png' }
    if(_.includes(MIME_CATEGORIES.sheet, mimeType))      { return '2_sheet.png' }
    if(_.includes(MIME_CATEGORIES.slide, mimeType))      { return '4_slide.png' }
    if(_.includes(MIME_CATEGORIES.pdf, mimeType))        { return '6_pdf.png' }
    if(_.includes(MIME_CATEGORIES.compressed, mimeType)) { return '7_zip.png' }
    if(mimeType.match(/^audio\//)) { return '8_audio.png' }
    if(mimeType.match(/^image\//)) { return '5_image.png' }
    if(mimeType.match(/^video\//)) { return '9_video.png' }
    return '10_misterious.png'
  }
}
