const dotenv = require('dotenv');
const mongoose = require('mongoose');
const mainVariablesModel = require('./src/schemas/mainVariables');
const { addModelData, getModelData, clearModelData } = require('./src/utils/databaseUtils');

dotenv.config();

const emptyVariablesRecord = {
    avatarCooldown: -1,
    avatarNumber: -1,
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

(async () => {
    console.log('Connecting to database...');
    await mongoose.connect(process.env.MONGO_URI)
        .then(async () => {
            if (collectionArgument === 'delete') {
                await clearModelData(mainVariablesModel);
                return;
            }

            console.log('Fetching data from mainVariables...');
            const variablesData = await getModelData(mainVariablesModel);

            if (variablesData.length !== 0) {
                if (collectionArgument !== 'override') {
                    console.log('DB is not empty! If you want to override data, pass "override" as a parameter');
                    return;
                }
                console.log('Overriding data...');
                await clearModelData(mainVariablesModel);
            }
            console.log('Adding empty record...');
            await addModelData(mainVariablesModel, emptyVariablesRecord);
            console.log('Finished adding empty record.');
        })
        .catch(async (e) => {
            console.log('There is an error occurred! Printing details:');
            console.error(e);
            console.log('Closing DB connection...');
            await mongoose.connection.close();
        })
        .finally(async () => {
            console.log('Closing DB connection...');
            await mongoose.connection.close();
            console.log('Done!');
        });
})();
