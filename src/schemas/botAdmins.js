const mongoose = require('mongoose');

const requireNumber = {
    type: Number,
    required: true,
};

const adminSchema = new mongoose.Schema({
    adminID: requireNumber,
});

module.exports = mongoose.model('botAdmins', adminSchema, 'botAdmins');
