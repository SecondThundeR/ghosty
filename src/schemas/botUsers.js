const mongoose = require('mongoose');

const requireString = {
    type: String,
    required: true,
};

const botUsersSchema = new mongoose.Schema({
    guildID: requireString,
    guildMembers: [{ type: String }],
});

module.exports = mongoose.model('botUsers', botUsersSchema, 'botUsers');
