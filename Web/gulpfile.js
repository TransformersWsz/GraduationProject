var gulp = require("gulp");
var browserSync = require('browser-sync');
var reload = browserSync.reload;
var nodemon = require('gulp-nodemon');

gulp.task("node", () => {
    nodemon({
        script: './bin/www',
        ext: 'js html',
        env: {
            'NODE_ENV': 'development'
        }
    });
});

gulp.task('server', ["node"], () => {
    var files = [
        'views/**/*.ejs',
        'routes/**/*.js',
        'public/**/*.*'
    ];

    //gulp.run(["node"]);
    browserSync.init(files, {
        proxy: 'http://localhost:3000',
        browser: 'chrome',
        notify: false,
        port: 4001 //这个是browserSync对http://localhost:3000实现的代理端口
    });

    gulp.watch(files).on("change", reload);
});