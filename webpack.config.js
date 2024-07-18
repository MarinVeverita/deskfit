const path = require('path');

module.exports = {
  entry: './assets/javascript/index.js',  // path to our input file
  output: {
    filename: 'index-bundle.js',  // output bundle file name
    path: path.resolve(__dirname, './main/static'),  // path to our Django static directory
  },
};