#!/usr/bin/env node
'use strict'
const _ = require('lodash')
const fs = require('fs')
const readline = require('readline')
const google = require('googleapis')
const googleAuth = require('google-auth-library')
const moment = require('moment')

const yargs = require('yargs')
  .example('$0 -t', 'Get an API token')
  .example('$0 -c foo@example.com', 'Fetch all events of foo@example.com')
  .option('t', {
    alias : 'token',
    describe: 'get new token',
    demand: false,
    nargs: 0,
    requiresArg: false
  })
  .option('c', {
    alias : 'calendar',
    describe: 'Calendar ID',
    type: 'string',
    nargs: 1,
    demand: false,
    requiresArg: true
  })
  .help()
const argv = yargs.argv

// If modifying these scopes, delete your previously saved credentials
// at ~/.credentials/calendar-nodejs-quickstart.json
const SCOPES = [
  'https://www.googleapis.com/auth/calendar.readonly',
  'https://www.googleapis.com/auth/drive.metadata.readonly'
]
const TOKEN_DIR = `${process.env.HOME || process.env.HOMEPATH ||
    process.env.USERPROFILE}/.credentials`
const TOKEN_PATH = `${TOKEN_DIR}/googleapps-ai-demo`


const getNewToken = (credentials) => {
  return new Promise((resolve, reject) => {
    const clientSecret = credentials.installed.client_secret
    const clientId = credentials.installed.client_id
    const redirectUrl = credentials.installed.redirect_uris[0]
    const auth = new googleAuth()
    const oauth2Client = new auth.OAuth2(clientId, clientSecret, redirectUrl)

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
        if (err) { return reject(err) }
        resolve(token)
      })
    })
  })
}


const storeToken = (token) => {
  return new Promise((resolve, reject) => {
    try { fs.mkdirSync(TOKEN_DIR) }
    catch (err) {
      if (err.code != 'EEXIST') { return reject(err) }
    }
    fs.writeFile(TOKEN_PATH, JSON.stringify(token), () => {
      console.log(`Token stored to ${TOKEN_PATH}`)
      resolve(token)
    })
  })
}


const authorize = (credentials) => {
  const clientSecret = credentials.installed.client_secret
  const clientId = credentials.installed.client_id
  const redirectUrl = credentials.installed.redirect_uris[0]
  const auth = new googleAuth()
  const oauth2Client = new auth.OAuth2(clientId, clientSecret, redirectUrl)

  return new Promise((resolve, reject) => {
    // Check if we have previously stored a token.
    fs.readFile(TOKEN_PATH, (err, token) => {
      if (err) { return reject('token cannot be found') } //getNewToken(oauth2Client, callback)

      oauth2Client.credentials = JSON.parse(token)
      resolve(oauth2Client)
    })
  })
}


const saveCalendarEvents = (auth) => {
  return new Promise((resolve, reject) => {
    google.calendar('v3').events.list({
      auth: auth,
      calendarId: argv.c,
      timeMin: moment('2000-01-01').toDate().toISOString(),
      timeMax: moment().toDate().toISOString(),
      maxResults: 100000,
      singleEvents: true,
      orderBy: 'startTime'
    }, (err, response) => {
      if (err) { return reject(err) }

      _.each(response.items, (event) => {
        fs.writeFile(`data/calendar/${event.id}.json`, JSON.stringify(event, null, 2))
      })
      console.log(`${response.items.length} calendar events saved`)

      resolve(response.items)
    })
  })
}

const loadSecret = () => {
  return new Promise((resolve, reject) => {
    fs.readFile('client_secret.json', (err, content) => {
      if(err) { return reject(`Error loading client secret file: ${err}`) }
      resolve(JSON.parse(content))
    })
  })
}


//
// Execute
//
if(argv.t) {
  loadSecret()
  .then(getNewToken)
  .then(storeToken)
  .catch(console.error)
}
else if(argv.c) {
  loadSecret()
  .then(authorize)
  .then(saveCalendarEvents)
  .catch(console.error)
}
else { yargs.showHelp() }
