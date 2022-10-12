// accessing entered query value
user_input = document.querySelector(".index header .query-box")
//accessing query btn
btn = document.querySelector(".index header .query-btn")
// accesses all songs elements
data = document.querySelectorAll(".caption h2")



// check if user click search 
btn.addEventListener("click", () => {
    // getting user input
    input = user_input.value
    // iterates over all titles 
    for (let i = 0; i < data.length; i++) {
        // hide all music-boxes
        data[i].parentElement.parentElement.parentElement.style.display = "none"
        // checks if input is a substring of a title
        if (data[i].textContent.includes(input)) {
            //only show the music-box wich match query
            data[i].parentElement.parentElement.parentElement.style.display = "block"
        }
    }
})


// ==========
// SONG PAGE
// ==========

// makes each song listen for click
arr = document.querySelectorAll(".img-fluid")
for (let i = 0; i < arr.length; i++) {
    arr[i].addEventListener("click", () => {
        // adds "song"  to url so that app loads the page
        window.location.href = `http://127.0.0.1:5000/song?comment=${arr[i].alt}`
    })
}

