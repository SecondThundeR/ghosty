const mongoose = require('mongoose');

const requireNumber = {
    type: Number,
    required: true,
};
const notRequiredString = {
    type: String,
    required: false,
};
const requireBoolean = {
    type: Boolean,
    required: true,
};

const mainVariablesSchema = new mongoose.Schema({
    avatarCooldown: requireNumber,
    botUptime: requireNumber,
    pollLocked: requireBoolean,
    rspActiveStatus: requireBoolean,
    shipActivatedStatus: requireBoolean,
    shipActiveStatus: requireBoolean,
    shipDate: notRequiredString,
    shipTextFull: notRequiredString,
    shipTextShort: notRequiredString,
});

module.exports = mongoose.model('mainVariables', mainVariablesSchema, 'mainVariables');
