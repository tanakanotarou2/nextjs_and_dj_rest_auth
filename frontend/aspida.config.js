module.exports = {
  input: 'src/api', // "input" of aspida is "output" for openapi2aspida
  outputEachDir: true, // Generate $api.ts in each endpoint directory
  openapi: {
    inputFile: 'http://localhost:8000/api/schema/',
  },
};
