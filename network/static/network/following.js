document.addEventListener('DOMContentLoaded', function(){
    ShowFollowingPosts()
});

let cont = 0;

function ShowFollowingPosts(){
    fetch(`/posts/following?cant=${cont}`).then(response => response.json()).then(posts => {
        console.log(posts)
        for(let i = 0; i < posts.length; i++){
            const crea = document.createElement('div')
            crea.innerHTML = `<div id="creator"><a type="hidden" href="/profile/prof?u=${posts[i].creator}">${posts[i].creator}</a></div><div class="content">${posts[i].content}</div><div class="date">${posts[i].created}</div><div><img src="https://logowik.com/content/uploads/images/like-heart2255.logowik.com.webp" height=10px>${posts[i].likes}</div>`
            document.querySelector('#container').appendChild(crea)
            
        }    
    })
}