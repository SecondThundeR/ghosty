const logoColors = [
    '#C9CBFF',
    '#7868E6',
    '#DEF4F0',
    '#DEF4F0',
    '#43658B',
    '#654062',
    '#132743',
    '#763857',
    '#ECA3F5',
    '#132C33',
    '#78C4D4',
    '#046582',
    '#822659',
    '#F1D1D0',
    '#1687A7',
    '#2A3D66',
];

function getRandomEmbedColor() {
    return logoColors[Math.floor(Math.random() * logoColors.length)];
}

exports.getRandomEmbedColor = getRandomEmbedColor;
