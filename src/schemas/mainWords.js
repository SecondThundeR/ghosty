const mongoose = require('mongoose');

const requireString = {
	type: String,
	required: true,
};

const mainWordsSchema = new mongoose.Schema({
	word: requireString,
});

module.exports = mongoose.model('mainWords', mainWordsSchema, 'mainWords');
