const mongoose = require('mongoose');

const requireString = {
    type: String,
    required: true,
};

const rouletteLoseWordsSchema = new mongoose.Schema({
    word: requireString,
});

module.exports = mongoose.model('rouletteLoseWords', rouletteLoseWordsSchema, 'rouletteLoseWords');
