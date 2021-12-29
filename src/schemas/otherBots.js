const mongoose = require('mongoose');

const requireString = {
    type: Number,
    required: true,
};

const otherBotsSchema = new mongoose.Schema({
    guildID: requireString,
    guildBots: [{ type: String }],
});

module.exports = mongoose.model('otherBots', otherBotsSchema, 'otherBots');
