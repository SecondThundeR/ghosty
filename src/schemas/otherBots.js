const mongoose = require('mongoose');

const requireString = {
    type: String,
    required: true,
};

const otherBotsSchema = new mongoose.Schema({
    guildID: requireString,
    guildBots: [{ type: String }],
});

module.exports = mongoose.model('otherBots', otherBotsSchema, 'otherBots');
