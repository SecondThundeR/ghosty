function formatTimeValue(s) {
    return (s < 10 ? '0' : '') + s;
}

function getFormattedTime(time) {
    const hours = formatTimeValue(Math.floor(time / (60 * 60)));
    const minutes = formatTimeValue(Math.floor(time % (60 * 60) / 60));
    const seconds = formatTimeValue(Math.floor(time % 60));
    return `**${hours}:${minutes}:${seconds}**`;
}

exports.getFormattedTime = getFormattedTime;
