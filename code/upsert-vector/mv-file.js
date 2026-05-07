// No need to require 'fs' if you've allowed it in environment variables.
// If you haven't, this will still throw 'disallowed'. 
// Ensure N8N_BLOCK_SVG_DECODING=false and NODE_FUNCTION_ALLOW_BUILTIN=fs,path are set.

const fs = require('fs').promises;
const path = require('path');

async function moveAllFiles(sourceFolder, destinationFolder) {
    const report = {
        moved: [],
        errors: []
    };

    try {
        await fs.mkdir(destinationFolder, { recursive: true });
        const items = await fs.readdir(sourceFolder, { withFileTypes: true });

        for (const item of items) {
            if (item.isFile()) {
                const sourcePath = path.join(sourceFolder, item.name);
                const destPath = path.join(destinationFolder, item.name);

                try {
                    await fs.rename(sourcePath, destPath);
                    report.moved.push(item.name);
                } catch (err) {
                    report.errors.push({ file: item.name, error: err.message });
                }
            }
        }
    } catch (err) {
        report.errors.push({ folder: sourceFolder, error: err.message });
    }

    return report;
}

// --- n8n Execution Wrapper ---
const source = "/home/node/.n8n-files/rag/newfiles";
const destination = "/home/node/.n8n-files/rag";

// We MUST await the function and return it in n8n format
const result = await moveAllFiles(source, destination);

// n8n requires an array of objects
return [
  {
    json: result
  }
];
