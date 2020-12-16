module.exports = {
    outputDir: 'dist',
    assetsDir: 'static',
    devServer: {
      proxy: {
        '^/api/*': {
          // Forward frontend dev server request for /api to fastapi dev server
          target: 'http://localhost:5000/',
        },
        '/docs*': {
          // Forward frontend dev server request for /api to fastapi dev server
          target: 'http://localhost:5000/',
      }
    }
  }
}