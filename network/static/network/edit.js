    function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function submit(id){
    const csrftoken = getCookie('csrftoken');
    let content = document.querySelector(`#text${id}`).value
    console.log(content) 
    fetch(`edit/${id}`, 
    {
        headers : {
            "X-CSRFToken": csrftoken
        },
        method :'POST',
        body : JSON.stringify({
            body: content
        })
    }).then(response => response.json()).then(data =>{document.querySelector(`#content${id}`).innerHTML = data})
    
}

function follow(){
    const user_id = document.querySelector('#id').value
    fetch(`/follow/${user_id}`).then(response => response.json()).then(cond => {
       console.log(cond)
       document.querySelector('#foll').innerHTML = cond.state
       document.querySelector('#followers').innerHTML = cond.followers
       document.querySelector('#following').innerHTML = cond.following
});
    
    }