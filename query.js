#!/usr/bin/env node
'use strict'
const _ = require('lodash')
const mkdirp = require('mkdirp')
const fs = require('fs')
const readline = require('readline')
const google = require('googleapis')
const googleAuth = require('google-auth-library')
const moment = require('moment')

const argv = require('yargs')
  .usage('Usage: $0 -c CALENDAR_ID')
  .example('$0 -c rsakai@reactive.co.jp', 'Fetch all events of rsakai@reactive.co.jp')
  .option('c', {
    alias : 'calendar',
    describe: 'Calendar ID',
    type: 'string',
    nargs: 1,
    demand: true,
    requiresArg: true
  })
  .help('help')
  .argv

// If modifying these scopes, delete your previously saved credentials
// at ~/.credentials/calendar-nodejs-quickstart.json
const SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
const TOKEN_DIR = `${process.env.HOME || process.env.HOMEPATH ||
    process.env.USERPROFILE}/.credentials/`
const TOKEN_PATH = `${TOKEN_DIR}calendar-nodejs-quickstart.json`


const authorize = (credentials, callback) => {
  const clientSecret = credentials.installed.client_secret
  const clientId = credentials.installed.client_id
  const redirectUrl = credentials.installed.redirect_uris[0]
  const auth = new googleAuth()
  const oauth2Client = new auth.OAuth2(clientId, clientSecret, redirectUrl)

  // Check if we have previously stored a token.
  fs.readFile(TOKEN_PATH, (err, token) => {
    if (err) {
      getNewToken(oauth2Client, callback)
    } else {
      oauth2Client.credentials = JSON.parse(token)
      callback(oauth2Client)
    }
  })
}

const getNewToken = (oauth2Client, callback) => {
  const authUrl = oauth2Client.generateAuthUrl({
    access_type: 'offline',
    scope: SCOPES
  })
  console.log('Authorize this app by visiting this url: ', authUrl)
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  })
  rl.question('Enter the code from that page here: ', code => {
    rl.close()
    oauth2Client.getToken(code, (err, token) => {
      if (err) {
        console.log('Error while trying to retrieve access token', err)
        return
      }
      oauth2Client.credentials = token
      storeToken(token)
      callback(oauth2Client)
    })
  })
}

const storeToken = (token) => {
  try {
    fs.mkdirSync(TOKEN_DIR)
  } catch (err) {
    if (err.code != 'EEXIST') {
      throw err
    }
  }
  fs.writeFile(TOKEN_PATH, JSON.stringify(token))
  console.log(`Token stored to ${TOKEN_PATH}`)
}

const listEvents = (auth) => {
  const calendar = google.calendar('v3')
  calendar.events.list({
    auth: auth,
    calendarId: argv.c,
    timeMin: moment('2000-01-01').toDate().toISOString(),
    timeMax: moment().toDate().toISOString(),
    maxResults: 100000,
    singleEvents: true,
    orderBy: 'startTime'
  }, (err, response) => {
    if (err) {
      console.log(`The API returned an error: ${err}`)
      return
    }

    const dataDir = `data/calendar/${argv.c}`
    mkdirp.sync(dataDir)

    _.each(response.items, (event) => {
      fs.writeFile(`${dataDir}/${event.id}.json`,
                   JSON.stringify(event, null, 2))
      const start = event.start.dateTime || event.start.date
      console.log('%s - %s', start, event.summary)
    })
  })
}

const loadSecret = () => {
  return new Promise((resolve, reject) => {
    fs.readFile('client_secret.json', (err, content) => {
      if(err) { return reject(`Error loading client secret file: ${err}`) }
      resolve(content)
    })
  })
}

loadSecret()
.then((secret) => {
  authorize(JSON.parse(secret), listEvents)
})
.catch(console.error)


