/**
 * Clean up a string by removing extra whitespace, tabs, and newlines.
 * @param {string} text
 * @returns {string}
 */
function cleanText(text) {
  return text.replace(/\s+/g, ' ').trim();
}

/**
 * Split a string into chunks of approx. `chunkSize` characters.
 * Does not split in the middle of a word.
 * @param {string} text
 * @param {number} chunkSize
 * @returns {string[]}
 */
function chunkText(text, chunkSize = 500) {
  const words = text.split(' ');
  const chunks = [];
  let chunk = '';

  for (const word of words) {
    if ((chunk + word).length <= chunkSize) {
      chunk += word + ' ';
    } else {
      chunks.push(chunk.trim());
      chunk = word + ' ';
    }
  }

  if (chunk.trim().length > 0) {
    chunks.push(chunk.trim());
  }

  return chunks;
}

/**
 * Generate a hash-based ID for a chunk of text (used as Pinecone vector ID).
 * @param {string} text
 * @returns {string}
 */
function generateId(text) {
  let hash = 0;
  for (let i = 0; i < text.length; i++) {
    hash = (hash << 5) - hash + text.charCodeAt(i);
    hash |= 0; // Convert to 32bit integer
  }
  return `chunk-${Math.abs(hash)}`;
}

module.exports = {
  cleanText,
  chunkText,
  generateId
};
