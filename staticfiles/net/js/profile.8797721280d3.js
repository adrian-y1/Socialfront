document.addEventListener('DOMContentLoaded', () => {
    const csrftoken = document.querySelector('input[name=csrfmiddlewaretoken]').value

    let form = document.getElementById('follow-form')
    if(form != null){
        form.onsubmit = function (e) {
        e.preventDefault()
        url = `/follow/${this.dataset.user_id}`

        fetch(url, {
            method: 'PUT',
            headers: {
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({
                follower: this.dataset.current_user
            })
        })
        .then(res => res.json())
        .then(data => {

            for (i=0; i<form.elements.length; i++){
                let followersNum = document.querySelector('#followers-num')
                let layoutNum = document.querySelector('#layout-user-followings')
                
                if(form.elements[i].value === 'Unfollow'){
                    form.elements[i].value = 'Follow'
                    followersNum.innerHTML = parseInt(data.follower)
                } else {
                    form.elements[i].value = 'Unfollow'
                    followersNum.innerHTML = parseInt(data.follower)
                    document.querySelectorAll('.suggestion-users').forEach(user => {
                        if(user.dataset.id === this.dataset.user_id){
                            user.remove();
                        }
                    })
                }
            }
        })
        .catch(error => {
            console.log("ERROR: ", error)
        })
    }
    }
    const modal = document.querySelector('.profile-modal')
    const modalBtn = document.querySelector('.camera-btn')
    const modalCancel = document.getElementById('profile-cancel')
    if(modalBtn !== null){
        modalBtn.onclick = () => {
            modal.style.display = 'block'
        }
    }
    if(modalCancel !== null){
        modalCancel.onclick = () => {
            modal.style.display = 'none'
        }
    }
    window.onclick = (e) => {
        if(e.target == modal){
            modal.style.display = 'none'
        }
    }
})