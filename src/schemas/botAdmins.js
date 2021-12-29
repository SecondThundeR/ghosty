const mongoose = require('mongoose');

const requireString = {
    type: String,
    required: true,
};

const adminSchema = new mongoose.Schema({
    adminID: requireString,
});

module.exports = mongoose.model('botAdmins', adminSchema, 'botAdmins');
