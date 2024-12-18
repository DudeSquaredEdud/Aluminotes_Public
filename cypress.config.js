const { defineConfig } = require('cypress');

module.exports = defineConfig({
    e2e: {
        // We've imported your old cypress plugins here.
        // You may want to clean this up later by importing these.
        setupNodeEvents(on, config) {
            // implement node event listeners here
        },
        baseUrl: 'http://127.0.0.1:8000/',
        viewportHeight: 768,
        viewportWidth: 1024,
        supportFile: false,
    },
});
