const path = require('path');
const webpack = require('webpack');
const sass = require('sass');

const staticDir = path.resolve(__dirname, 'pattern_library', 'static', 'pattern_library');

module.exports = {
    entry: path.join(staticDir, 'src', 'js', 'app.js'),
    output: {
        path: path.join(staticDir, 'dist'),
        filename: 'bundle.js',
        publicPath: './dist'
    },
    module: {
        rules: [
            {
                test: /\.js$/,
                use: {
                    loader: 'babel-loader',
                }
            },
            {
                test: /\.scss$/,
                use: [
                    {
                        loader: 'style-loader' // creates style nodes from JS strings
                    },
                    {
                        loader: 'css-loader' // translates CSS into CommonJS
                    },
                    {
                        loader: 'sass-loader', // compiles Sass to CSS
                        options: {
                            implementation: sass,
                            sassOptions: {
                                outputStyle: 'compressed',
                            },
                        },
                    }
                ]
            }
        ]
    },
    plugins: [
        // Rather than import the entire contents of the
        // highlight lib (which includes languages we’re not using)
        // you can just import the languages you want to highlight,
        // therefore drastically reducing the bundle size
        new webpack.ContextReplacementPlugin(
            /highlight\.js\/lib\/languages$/,
            new RegExp(`^./(${['django', 'yaml'].join('|')})$`)
        )
    ],
};
