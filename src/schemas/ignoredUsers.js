const mongoose = require('mongoose');

const requireNumber = {
    type: Number,
    required: true,
};

const ignoredUsersSchema = new mongoose.Schema({
    userID: requireNumber,
});

module.exports = mongoose.model('ignoredUsers', ignoredUsersSchema, 'ignoredUsers');
