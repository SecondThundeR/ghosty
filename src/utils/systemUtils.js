const os = require('os');

class SystemUtils {
    static getSystemData() {
        return {
            'OSName': os.version(),
            'OSVersion': os.release(),
            'hostName': os.hostname(),
            'hostCPU': os.cpus()[0]['model'],
            'hostArch': os.arch(),
        };
    }

    static getSystemDataMessage() {
        const systemData = SystemUtils.getSystemData();
        return `Система: **${systemData['OSName']}** *(${systemData['OSVersion']})*`
            + `\nНазвание ПК: **${systemData['hostName']}**`
            + `\nПроцессор: **${systemData['hostCPU']}**`
            + `\nАрхитектура: **${systemData['hostArch']}**`;
    }
}

exports.SystemUtils = SystemUtils;
