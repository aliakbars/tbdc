var gulp = require('gulp');
var data = require('gulp-data');
var jade = require('gulp-jade');
var gutil = require('gulp-util');
var webpack = require('webpack');
var webpackConfig = require('./webpack.config.js');

gulp.task('jade', function(event) {
    return gulp.src('jade/*.jade')
        .pipe(data(function(file) {
            return require('./dist/patients.json')
        }))
        .pipe(jade({pretty: true}))
        .pipe(gulp.dest('.'))
});

gulp.task('webpack', function(done) {
    webpack(webpackConfig).run(function(err, stats) {
        if (err) {
          gutil.log('Error', err);
        } else {
          // gutil.log(stats.toString());
        }
        done();
    });
});

gulp.task('default', ['jade', 'webpack']);