class StringUtils {
    static reverseString(str) {
        return str.split('').reverse().join('');
    }
}

exports.StringUtils = StringUtils;
