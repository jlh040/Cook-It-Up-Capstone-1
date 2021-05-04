function randomRGB() {
    let red = Math.floor(Math.random() * 256);
    let green = Math.floor(Math.random() * 256);
    let blue = Math.floor(Math.random() * 256);

    return `rgb(150, ${green}, ${blue})`
}

const $cuisineCard = $('.cuisine-card');

setInterval(() => {
    $cuisineCard.css('background-color', randomRGB)
}, 400)