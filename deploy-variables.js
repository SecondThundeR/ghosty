const mongoose = require('mongoose');
const dotenv = require('dotenv');
const mainVariablesSchema = require('./src/schemas/mainVariables');

dotenv.config();

const emptyVariablesRecord = {
    avatarCooldown: 0,
    botUptime: 0,
    pollLocked: false,
    rspActiveStatus: false,
    shipActivatedStatus: false,
    shipActiveStatus: false,
    shipDate: '',
    shipTextFull: '',
    shipTextShort: '',
};
const args = process.argv.slice(2);
const collectionArgument = args[0] || '';

async function clearMainVariables() {
    await mainVariablesSchema.deleteMany({}, (err) => {
        if (err) console.error(err);
    }).clone().catch((err) => console.error(err));
    console.log('Cleared out mainVariables!');
}

async function fetchMainVariablesData() {
    return await mainVariablesSchema.find({}, (err) => {
        if (err) console.error(err);
    }).clone().catch((err) => console.error(err));
}

(async () => {
    console.log('Connecting to database...');
    await mongoose.connect(process.env.MONGO_URI)
        .then(async () => {
            if (collectionArgument === 'delete') {
                await clearMainVariables();
                return;
            }

            console.log('Fetching data from mainVariables...');
            const variablesData = await fetchMainVariablesData();

            if (variablesData.length != 0) {
                if (collectionArgument !== 'override') {
                    console.log('DB is not empty! If you want to override data, pass "override" as a parameter');
                    return;
                }
                console.log('Overriding data...');
                await clearMainVariables();
            }
            console.log('Adding empty record...');
            await new mainVariablesSchema(emptyVariablesRecord).save();
            console.log('Finished adding empty record.');
        })
        .catch(async (e) => {
            console.log('There is an error occured! Printing details:');
            console.error(e);
            console.log('Closing DB connection...');
            await mongoose.connection.close();
            return;
        })
        .finally(async () => {
            console.log('Closing DB connection...');
            await mongoose.connection.close();
            console.log('Done!');
        });
})();
