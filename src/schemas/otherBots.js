const mongoose = require('mongoose');

const requireNumber = {
    type: Number,
    required: true,
};

const otherBotsSchema = new mongoose.Schema({
    botID: requireNumber,
});

module.exports = mongoose.model('otherBots', otherBotsSchema, 'otherBots');
