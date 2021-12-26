const mongoose = require('mongoose');

const requireString = {
    type: String,
    required: true,
};

const rouletteZeroWordsSchema = new mongoose.Schema({
    word: requireString,
});

module.exports = mongoose.model('rouletteZeroWords', rouletteZeroWordsSchema, 'rouletteZeroWords');
