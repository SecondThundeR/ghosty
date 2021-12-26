const mongoose = require('mongoose');

const requireNumber = {
    type: Number,
    required: true,
};

const blockedUsersSchema = new mongoose.Schema({
    blockedUserID: requireNumber,
});

module.exports = mongoose.model('botBlockedUsers', blockedUsersSchema, 'botBlockedUsers');
