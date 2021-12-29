const mongoose = require('mongoose');

const requireString = {
    type: String,
    required: true,
};

const blockedUsersSchema = new mongoose.Schema({
    blockedUserID: requireString,
});

module.exports = mongoose.model('botBlockedUsers', blockedUsersSchema, 'botBlockedUsers');
