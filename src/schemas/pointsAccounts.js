const mongoose = require('mongoose');

const requireNumber = {
    type: Number,
    required: true,
};
const requireString = {
    type: String,
    required: true,
};
const requireBoolean = {
    type: Boolean,
    required: true,
};

const pointsAccountsSchema = new mongoose.Schema({
    dailyPointsDate: requireString,
    isDeleted: requireBoolean,
    pointsBalance: requireNumber,
    rouletteActiveStatus: requireBoolean,
    userID: requireNumber,
});

module.exports = mongoose.model('pointsAccounts', pointsAccountsSchema, 'pointsAccounts');
