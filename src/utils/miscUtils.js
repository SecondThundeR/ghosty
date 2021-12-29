function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function getRandomNumber(lowNum, highNum) {
    if (lowNum > highNum || (lowNum < 0 || highNum < 0)) return null;
    return Math.floor(Math.random() * (highNum - lowNum)) + lowNum;
}


exports.delay = delay;
exports.getRandomNumber = getRandomNumber;
