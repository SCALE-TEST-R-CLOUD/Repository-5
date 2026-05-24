const core = require('@actions/core');
const fs = require('fs');

async function run() {
  try {
    const input = core.getInput('example-input');
    console.log(`Echo: ${input}`);
    fs.writeFileSync('artifact.txt', `Artifact content: ${input}\n`);
    console.log('artifact.txt created.');
  } catch (error) {
    core.setFailed(error.message);
  }
}

run();
