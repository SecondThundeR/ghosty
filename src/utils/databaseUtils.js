const mainVariablesModel = require('../schemas/mainVariables');
const botUsersModel = require('../schemas/botUsers');
const ignoredUsersModel = require('../schemas/ignoredUsers');
const otherBotsModel = require('../schemas/otherBots');

const usersData = {
    guildID: null,
    guildMembers: null,
};
const botsData = {
    guildID: null,
    guildBots: null,
};

class DatabaseUtils {
    static async addModelData(model, data) {
        await new model(data)
            .save().catch((err) => console.error(err));
    }

    static async getModelData(model) {
        return await model.find({}, (err) => {
            if (err) console.error(err);
        }).clone().catch((err) => console.error(err));
    }

    static async updateAvatarData(options) {
        let filter, update;
        if (options.isAvatarCooldown) {
            filter = { avatarCooldown: options.oldData };
            update = { avatarCooldown: options.newData };
        }
        else {
            filter = { avatarNumber: options.oldData };
            update = { avatarNumber: options.newData };
        }
        await mainVariablesModel.findOneAndUpdate(filter, update);
    }

    static async updateMemberList(client) {
        await DatabaseUtils.clearModelData(botUsersModel);
        await DatabaseUtils.clearModelData(otherBotsModel);
        const ignoredUsersData = await DatabaseUtils.getModelData(ignoredUsersModel);
        const ignoredUsersID = DatabaseUtils.getIgnoredUsersID(ignoredUsersData);

        for (const guild of client.guilds.cache) {
            const guildID = guild[0];
            usersData['guildID'] = guildID;
            botsData['guildID'] = guildID;
            usersData['guildMembers'] = [];
            botsData['guildBots'] = [];

            const users = await guild[1].members.fetch({ force: true });

            for (const user of users) {
                const memberID = user[0];
                if (ignoredUsersID.includes(memberID)) continue;

                if (user[1].user.bot === false) {
                    usersData['guildMembers'].push(memberID);
                }
                else {
                    botsData['guildBots'].push(memberID);
                }
            }

            await DatabaseUtils.addModelData(botUsersModel, usersData);
            await DatabaseUtils.addModelData(otherBotsModel, botsData);
        }
    }

    static getIgnoredUsersID(ignoredUsersData) {
        const usersID = [];
        for (const item of ignoredUsersData) {
            usersID.push(item.userID);
        }
        return usersID;
    }

    static async clearModelData(model) {
        await model.deleteMany({}, (err) => {
            if (err) console.error(err);
        }).clone().catch((err) => console.error(err));
    }
}

exports.DatabaseUtils = DatabaseUtils;
