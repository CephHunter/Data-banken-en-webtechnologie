'use strict';
const gulp = require('gulp');
const sass = require('gulp-sass');
const plumber = require('gulp-plumber');
const postcss = require('gulp-postcss');
const autoprefixer = require('autoprefixer');
const rename = require("gulp-rename");
const sourcemaps = require('gulp-sourcemaps');

function watchFiles(cb) {
    gulp.watch("css/src/**/*.scss", css);
    cb();
}

function css() {
    return gulp.src("css/src/main.scss")
        .pipe(plumber())
        .pipe(sourcemaps.init())
        .pipe(sass().on('error', sass.logError))
        .pipe(postcss([ autoprefixer() ]))
        .pipe(sourcemaps.write())
        .pipe(rename('style.css'))
        .pipe(gulp.dest('./css'));
}

module.exports = {
    default: gulp.series(css, watchFiles)
}