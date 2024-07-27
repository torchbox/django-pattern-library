const path = require('path');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

const staticDir = path.resolve(__dirname, 'pattern_library', 'static', 'pattern_library');

module.exports = {
    entry: path.join(staticDir, 'src', 'js', 'app.js'),
    output: {
        path: path.join(staticDir, 'dist'),
        filename: 'bundle.js',
        publicPath: './dist'
    },
    plugins: [new MiniCssExtractPlugin()],
    module: {
        rules: [
            {
                test: /\.(js|ts)x?$/,
                loader: 'ts-loader',
            },
            {
                test: /\.scss$/,
                use: [
                    MiniCssExtractPlugin.loader,
                    'css-loader',
                    {
                        loader: 'sass-loader', // compiles Sass to CSS
                        options: {
                            sassOptions: {
                                outputStyle: 'compressed',
                            },
                        },
                    }
                ]
            }
        ]
    },
};
