const mongoose = require('mongoose');

const requireString = {
    type: String,
    required: true,
};

const markovWordsSchema = new mongoose.Schema({
    word: requireString,
});

module.exports = mongoose.model('markovWords', markovWordsSchema, 'markovWords');
