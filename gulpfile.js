var gulp = require('gulp');
var data = require('gulp-data');
var jade = require('gulp-jade');

gulp.task('jade', function(event) {
    return gulp.src("jade/*.jade")
        .pipe(data(function(file) {
            return require('./dist/patients.json')
        }))
        .pipe(jade({pretty: true}))
        .pipe(gulp.dest("."))
});

gulp.task('default', ['jade']);