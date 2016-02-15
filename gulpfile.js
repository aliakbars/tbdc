var gulp = require('gulp');
var jade = require('gulp-jade');

gulp.task('jade', function(event) {
    return gulp.src("jade/*.jade")
        .pipe(jade({pretty: true}))
        .pipe(gulp.dest("."))
});

gulp.task('default', ['jade']);