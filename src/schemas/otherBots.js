const mongoose = require('mongoose');

const requireNumber = {
    type: Number,
    required: true,
};

const otherBotsSchema = new mongoose.Schema({
    guildID: requireNumber,
    guildBots: [{ type: Number }],
});

module.exports = mongoose.model('otherBots', otherBotsSchema, 'otherBots');
