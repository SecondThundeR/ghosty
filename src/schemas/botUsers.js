const mongoose = require('mongoose');

const requireNumber = {
    type: Number,
    required: true,
};

const botUsersSchema = new mongoose.Schema({
    guildID: requireNumber,
    guildMembers: [{ type: Number }],
});

module.exports = mongoose.model('botUsers', botUsersSchema, 'botUsers');
