const { createProxyMiddleware } = require('http-proxy-middleware');

// https://github.com/chimurai/http-proxy-middleware/issues/40#issuecomment-249430255
const restream = (proxyReq, req) => {
    if (req.body) {
        const bodyData = JSON.stringify(req.body);
        proxyReq.setHeader('Content-Type', 'application/json');
        proxyReq.setHeader('Content-Length', Buffer.byteLength(bodyData));
        proxyReq.write(bodyData);
    }
};

/**
 * Initialises a http-proxy-middleware for Storybook to talk to Django without CORS issues.
 * @param {object} options options
 * @param {string} options.origin where Django runs, for example http://localhost:8000
 * @param {string} options.apiPath API endpoint to render patterns (/pattern-library/api/v1/render-pattern)
 * @param {function} options.proxy http-proxy-middleware module
 */
const createDjangoAPIMiddleware = (options) => {
    const { proxy, apiPath, origin } = options;
    const createProxy = proxy || createProxyMiddleware;
    const middleware = (router) => {
        router.use(
            apiPath,
            createProxy({
                target: origin,
                changeOrigin: true,
                onProxyReq: restream,
            }),
        );
    };

    return middleware;
};

module.exports = {
    createDjangoAPIMiddleware,
};


module.exports = createDjangoAPIMiddleware({
    origin: 'http://localhost:8003',
    apiPath: ['/render-pattern/', '/static/', '/api/v1/'],
});
