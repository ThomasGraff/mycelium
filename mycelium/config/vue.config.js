const path = require('path');
const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: true,
  configureWebpack: {
    resolve: {
      alias: {
        '@': path.resolve(__dirname, '../src'),
      },
    },
    module: {
      rules: [
        {
          test: /\.js$/,
          exclude: /node_modules/,
          use: {
            loader: 'babel-loader',
            options: {
              presets: ['@babel/preset-env']
            }
          }
        }
      ]
    }
  },
  pluginOptions: {
    vuetify: {
      // https://github.com/vuetifyjs/vuetify-loader/tree/next/packages/vuetify-loader
    }
  },
  devServer: {
    proxy: {
      '/api': {
        target: process.env.BACKEND_URL,
        changeOrigin: true,
        pathRewrite: {
          '^/api': ''
        }
      },
    }
  },
  pages: {
    index: {
      entry: path.resolve(__dirname, '../src/main.js'),
      template: path.resolve(__dirname, '../public/index.html'),
      filename: 'index.html',
      title: 'Mycelium',
    },
  },
})
