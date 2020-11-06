module.exports = {
  transpileDependencies: [
    'vuetify'
  ],
  configureWebpack: {
    devServer: {
      headers: { 'Access-Control-Allow-Origin': '*' },
      proxy: 'http://localhost:8000'
    }
  }
}
