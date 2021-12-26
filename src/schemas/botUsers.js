const mongoose = require('mongoose');

const requireNumber = {
	type: Number,
	required: true,
};

const botUsersSchema = new mongoose.Schema({
	userID: requireNumber,
});

module.exports = mongoose.model('botUsers', botUsersSchema, 'botUsers');
