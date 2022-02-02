class TimeUtils {
    static formatTimeValue(s) {
        return (s < 10 ? '0' : '') + s;
    }

    static getFormattedTime(time) {
        const hours = TimeUtils.formatTimeValue(Math.floor(time / (60 * 60)));
        const minutes = TimeUtils.formatTimeValue(Math.floor(time % (60 * 60) / 60));
        const seconds = TimeUtils.formatTimeValue(Math.floor(time % 60));
        return `**${hours}:${minutes}:${seconds}**`;
    }
}

exports.TimeUtils = TimeUtils;
