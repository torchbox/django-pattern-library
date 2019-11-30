const path = require('path');
const webpack = require('webpack');

const staticDir = path.resolve(__dirname, 'pattern_library', 'static', 'pattern_library');

module.exports = {
    entry: path.join(staticDir, 'src', 'js', 'app.js'),
    output: {
        path: path.join(staticDir, 'dist'),
        filename: 'bundle.js',
    },
    module: {
        rules: [
            {
                test: /\.js$/,
                use: {
                    loader: 'babel-loader',
                    options: { presets: ['env'] }
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
                        loader: 'sass-loader' // compiles Sass to CSS
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
    devServer: {
        hot: true,
        host: '0.0.0.0',
        port: process.env.WDS_PORT,
        publicPath: process.env.WDS_PUBLIC_PATH,
        open: true,
        openPage: 'pattern-library/',
        index: '',
        proxy: {
            '/': {
                target: process.env.WDS_PROXY_TARGET
            }
        }
    }
};
