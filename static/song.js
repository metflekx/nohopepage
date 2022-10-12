function create_music(title) {
    //creates music-box element
    const music_box = document.createElement("div")
    music_box.classList.add("music_box")
    //nests all html inside music-box
    music_box.innerHTML = `
            <figure>
                <img src = "../static/images/${title}.jpeg" alt="${title}" class="img-fluid">

                <figcaption class="caption d-flex align-items-center justify-content-center">
                <h2> ${title} </h2>
                </figcaption>
            </figure>
            
            <audio controls>
                <source src = "../static/music/${title}.mp3">
            </audio>
            `
    //adds music_box into body
    document.querySelector(".song").appendChild(music_box)
    return 0
}


// getting title from url
title = window.location.search.slice(9)
// creating post passing in title
create_music(title)
