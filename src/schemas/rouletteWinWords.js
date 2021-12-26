const mongoose = require('mongoose');

const requireString = {
    type: String,
    required: true,
};

const rouletteWinWordsSchema = new mongoose.Schema({
    word: requireString,
});

module.exports = mongoose.model('rouletteWinWords', rouletteWinWordsSchema, 'rouletteWinWords');
