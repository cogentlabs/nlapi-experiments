'use strict'
const gulp    = require('gulp')
const plumber = require('gulp-plumber')
const webpack = require('webpack-stream')

gulp.task('default', ['asset', 'webpack'])

gulp.task('asset', () => {
  return gulp.src(
    ['assets/**'],
    {base: 'assets'}
  ).pipe(gulp.dest('dist'))
})

gulp.task('webpack', () => {
  return gulp.src('src/main.js')
    .pipe(plumber())
    .pipe(webpack({
      watch: true,
      devtool: 'source-map',
      output: { filename: 'bundle.js' },
      module: {
        loaders: [
          {
            test: /.js?$/,
            loader: 'babel-loader',
            exclude: /node_modules/,
            query: {
              presets: ['es2015', 'react']
            }
          }
        ]
      }
    }))
    .pipe(gulp.dest('dist'))
})
