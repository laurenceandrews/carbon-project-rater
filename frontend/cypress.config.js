const { defineConfig } = require("cypress");

module.exports = defineConfig({
  projectId: 'nywh4z',
  e2e: {
    baseUrl: 'http://localhost:3000',

    specPattern: 'cypress/integration/**/*spec.js',

    // Ignore example test files
    excludeSpecPattern: '**/1-getting-started/**/*.*',
    
    setupNodeEvents(on, config) {
      // implement node event listeners here
    },
  },
});