const csrftoken = document.querySelector('input[name=csrfmiddlewaretoken]').value


// ---------- Edit Post Start ---------- \\
function editPost(post_id) {
    let modalDescription = document.querySelector('#myTextarea');
    let form = document.querySelector('#edit-form');
    form.onsubmit = (e) => {
        e.preventDefault();
        url = `/edit/${post_id}`

        fetch(url, {
            method: 'PUT',
            headers: {
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({
                description: modalDescription.value
            })
        })
        .then(response => response.json())
        
        .catch(error => console.log("ERROR", error))
        const updateDescription = document.querySelectorAll('#update-desc');
        updateDescription.forEach(desc => {
            if(desc.dataset.id === post_id){
                desc.innerHTML = modalDescription.value
            }
        })
    }
}
// ---------- Edit Post End ---------- \\

// ---------- Dropdown Start ---------- \\
function toggleDropdown(e){
    const content = e.parentNode.getElementsByClassName('index-dropdown-content')[0]
    content.classList.toggle('show')
}

const indexDropdown = document.querySelectorAll('.index-dropdown')
indexDropdown.forEach(dropdown => {
    dropdown.onclick = function (e) {
        const content = this.parentNode.getElementsByClassName('index-dropdown-content')[0]
        if(content.style.display === 'block'){
            content.style.display = 'none'
        } else {
            content.style.display = 'block'
        }
    }
})

window.addEventListener('mouseup', e => {
    indexDropdown.forEach(drop => {
        if(e.target != drop){
            drop.parentNode.getElementsByClassName('index-dropdown-content')[0].style.display = 'none'
        }
    })
})

// ---------- Dropdown End ---------- \\



document.addEventListener('DOMContentLoaded', () => {

    // ---------- Edit Post Start ---------- \\
    document.querySelectorAll("#edit-btn").forEach(button => {
        button.onclick = function() {
            editPost(this.dataset.id)

            // Update the button dataset of text with the description of the post
            const updateDesc = document.querySelectorAll('#update-desc');
            updateDesc.forEach(update => {
                if(update.dataset.id === this.dataset.id){
                    this.dataset.text = update.innerHTML
                }
            })
             // assign the current button's text dataset to the textarea 
            document.querySelector("#myTextarea").value = this.dataset.text
        }
    })
    // ---------- Edit Post End ---------- \\

    // ---------- Like Post Start ---------- \\
    document.querySelectorAll('.like-form').forEach(form => {
        form.onsubmit = function (e) {
            e.preventDefault();

            let user_id = this.dataset.user_id
            let input = this.getElementsByTagName('button')[0]
            let likeUrl = `/like/${this.dataset.id}`
            
            fetch(likeUrl, {
                method: "PUT",
                headers: {
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({
                    likes: user_id
                })
            })
            .then(response => response.json())
            .then(data => {

                let count = document.querySelectorAll('.like-count')
                count.forEach(c => {
                    if(this.dataset.id === c.dataset.id ){
                        c.innerHTML = data.likes
                    }
                })
            })
            .catch(error => console.log("LIKE ERROR:", error))

            const el = document.createElement('i');

            if(input.value === 'Like'){
                input.removeChild(input.getElementsByTagName('i')[0])
                el.className = 'bi bi-heart-fill'
                el.style.color = 'rgb(218, 86, 108)'
                input.appendChild(el)
                input.value = 'Unlike'
            } else {
                input.removeChild(input.getElementsByTagName('i')[0])
                el.className = 'bi bi-heart'
                input.appendChild(el)
                input.value = 'Like'
            }

        }
    })
    // ---------- Like Post End ---------- \\

    const indexTextarea = document.querySelector('.index-textarea')
    if(indexTextarea != null){
        indexTextarea.focus();
        const indexPostBtn = document.querySelector('.post-btn')

        indexTextarea.onkeydown = e => {
            if(e.keyCode === 13){
                e.preventDefault();
                indexPostBtn.click();
            }
        }
    }
})

// ---------- Like Comment Start ---------- \\
document.addEventListener('DOMContentLoaded', () => {

    document.querySelectorAll('.comment-like-form').forEach(function(commentForm) {
        commentForm.onsubmit = function (event) {
            event.preventDefault();

            let c_user_id = this.dataset.user_id
            let formBtn = this.getElementsByTagName('button')[0]
            let commentLikeUrl = `/comment/like/${this.dataset.id}`

            fetch(commentLikeUrl, {
                method: "PUT",
                headers: {
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({
                    likes: c_user_id
                })
            })
            .then(res => res.json())
            .then(data => {
                let likeCount = document.querySelectorAll('.comment-like-count')
                likeCount.forEach(count => {
                    if(this.dataset.id === count.dataset.id ){
                        count.innerHTML = data.likes
                    }
                })
            })
            .catch(error => console.log("LIKE ERROR:", error))

            const newEl = document.createElement('i')

            if(formBtn.value == 'Like'){
                formBtn.removeChild(formBtn.getElementsByTagName('i')[0])
                newEl.className = 'bi bi-heart-fill'
                newEl.style.color = 'rgb(218, 86, 108)'
                formBtn.appendChild(newEl)
                formBtn.value = 'Unlike'
            } else {
                formBtn.removeChild(formBtn.getElementsByTagName('i')[0])
                newEl.className = 'bi bi-heart'
                formBtn.appendChild(newEl)
                formBtn.value = 'Like'
            }
        }
    })
    const commentTextarea = document.querySelector('.post-comment-textarea')
    if(commentTextarea != null){
        commentTextarea.focus();
        const commentPostBtn = document.querySelector('.comment-btn')

        commentTextarea.onkeydown = e => {
            if(e.keyCode === 13){
                e.preventDefault();
                commentPostBtn.click();
            }
        }
    }
        const postDropdown = document.querySelectorAll('.post-dropdown')
        postDropdown.forEach(dropdown => {
            dropdown.onclick = function (e) {
                const content = this.parentNode.getElementsByClassName('post-dropdown-content')[0]
                if(content.style.display === 'block'){
                    content.style.display = 'none'
                } else {
                    content.style.display = 'block'
                }
            }
        })

        window.addEventListener('mouseup', e => {
            postDropdown.forEach(drop => {
                if(e.target != drop){
                    drop.parentNode.getElementsByClassName('post-dropdown-content')[0].style.display = 'none'
                }
            })
        })

        // ---------- Dropdown End ---------- \\

})
// ---------- Like Comment End ---------- \\


