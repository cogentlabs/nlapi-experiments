#!/usr/bin/env node
'use strict'
const _ = require('lodash')
const path = require('path')
const fsp = require('fs-promise')
const axios = require('axios')

const argv = require('yargs')
  .example('$0 foo.json', 'classify and save Google calendar event by NL API')
  .example('$0 -f foo.json', 'classify a plain text file by NL API')
  .option('f', {
    alias : 'file',
    describe: 'classify a plain text file',
    demand: false,
    nargs: 1,
    requiresArg: true
  })
  .help()
  .argv

const ENTITIES_API_ENDPOINT = `https://language.googleapis.com/v1alpha1/documents:analyzeEntities?key=${process.env.GOOGLE_API_KEY}`
const ANNOTATE_API_ENDPOINT = `https://language.googleapis.com/v1alpha1/documents:annotateText?key=${process.env.GOOGLE_API_KEY}`

const saveEntities = (filename, text) => {
  if(_.isEmpty(text)) { return }

  analyzeEntities(text)
  .then((result) => {
    if(!_.isEmpty(result.entities)) {
      fsp.writeFile(filename, JSON.stringify(result, null, 2))
      .then(() => { console.log(`Entity saved : ${filename}`) })
    }
  })
  .catch((err) => {
    console.error(`ERROR : ${filename}`)
    console.error(err)
  })
}


const analyzeEntities = (text) => {
  return new Promise((resolve, reject) => {
    axios.post(ENTITIES_API_ENDPOINT, {
      document: {type: 'PLAIN_TEXT', content: text},
      encoding_type: 'UTF8'
    })
    .then((res) => { resolve(res.data) })
    .catch((res) => { reject(res.data) })
  })
}

const annotateText = (text) => {
  return new Promise((resolve, reject) => {
    axios.post(ANNOTATE_API_ENDPOINT, {
      document: {type: 'PLAIN_TEXT', content: text},
      features: {
        extractSentences: true,
        extractTokens: true,
        extractEntities: true,
        extractDocumentSentiment: true
      },
      encoding_type: 'UTF8'
    })
    .then((res) => { resolve(res.data) })
    .catch((res) => { reject(res.data) })
  })
}


const processPlainTextFile = (filename) => {
  fsp.readFile(filename, {encoding:'utf8'})
  .then(annotateText)
  .then((content) => { console.log(JSON.stringify(content, null, 2)) })
  .catch(console.error)
}

const processCalendarEvents = () => {
  argv._.forEach((fileName) => {
    const basename = path.basename(fileName, '.json')
    const savePath = `data/calendar-entities`

    fsp.readFile(fileName, {encoding:'utf8'})
    .then((content) => JSON.parse(content))
    .then((content) => {
      saveEntities(`${savePath}/${basename}.summary.json`, content.summary)
      saveEntities(`${savePath}/${basename}.location.json`, content.location)
      saveEntities(`${savePath}/${basename}.description.json`, content.description)
    })
    .catch(console.error)
  })
}


if(argv.f) { processPlainTextFile(argv.f) }
else { processCalendarEvents() }
