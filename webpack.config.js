const path = require('path');

const staticDir = path.resolve(
    __dirname,
    'pattern_library',
    'static',
    'pattern_library',
);

module.exports = {
    entry: path.join(staticDir, 'src', 'js', 'app.js'),
    output: {
        path: path.join(staticDir, 'dist'),
        filename: 'bundle.js',
        publicPath: './dist',
    },
    module: {
        rules: [
            {
                test: /\.js$/,
                use: {
                    loader: 'babel-loader',
                },
            },
            {
                test: /\.scss$/,
                use: [
                    {
                        loader: 'style-loader', // creates style nodes from JS strings
                    },
                    {
                        loader: 'css-loader', // translates CSS into CommonJS
                    },
                    {
                        loader: 'sass-loader', // compiles Sass to CSS
                        options: {
                            sassOptions: {
                                outputStyle: 'compressed',
                            },
                        },
                    },
                ],
            },
        ],
    },
};
