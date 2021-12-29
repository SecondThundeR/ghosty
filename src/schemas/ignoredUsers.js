const mongoose = require('mongoose');

const requireString = {
    type: String,
    required: true,
};

const ignoredUsersSchema = new mongoose.Schema({
    userID: requireString,
});

module.exports = mongoose.model('ignoredUsers', ignoredUsersSchema, 'ignoredUsers');
