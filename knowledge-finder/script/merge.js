#!/usr/bin/env node
'use strict'
const _ = require('lodash')
const path = require('path')
const glob = require('glob-fs')()
const fsp = require('fs-promise')
const argv = require('yargs')
  .example('$0 "data/calendar/*.json"', 'Merge files')
  .help()
  .argv


const output = []

_(argv._)
.map((pattern) => glob.readdirSync(pattern))
.flatten()
.each((filename) => {
  console.log(filename)
  const fileId = path.basename(filename, '.json')

  fsp.readFile(filename, {encoding: 'utf8'})
  .then(JSON.parse)
  .then((j) => {
    const record = _.pick(['id', 'status', 'summary', 'location'])
    record.start = moment(j.start.dateTime).unix()
    record.end = moment(j.end.dateTime).unix()

    console.log(record)
  })
})
