var webpack = require('webpack');

var config = {
  entry: {
    patients: './src/patientlist.jsx',
    tbform: './src/tbform.jsx'
  },

  // Add resolve.extensions.
  // '' is needed to allow imports without an extension.
  // Note the .'s before extensions as it will fail to match without!!!
  resolve: {
    extensions: ['', '.js', '.jsx']
  },

  module: {
    loaders: [
      // Set up jsx. This accepts js too thanks to RegExp
      {
        test: /\.jsx?$/,
        // Enable caching for improved performance during development
        // It uses default OS directory by default. If you need something
        // more custom, pass a path to it. I.e., babel?cacheDirectory=<path>
        loaders: ['babel?cacheDirectory,presets[]=react,presets[]=es2015']
      }
    ]
  },

  output: {
    path: 'dist/js',
    filename: '[name].js'
  }
};

module.exports = config;