document.addEventListener('DOMContentLoaded', () => {
    const followingSearch = document.querySelector('.followings-search')
    const followingCard = document.querySelectorAll('.followings-card')
    const user_instance = JSON.parse(document.getElementById('user_instance').textContent)

    all_followings = []

    followingSearch.addEventListener('input', e => {
        const val = e.target.value.toLowerCase();
        for(i=0; i < all_followings.length; i++){
            if(all_followings[i].includes(val)){
                followingCard[i].style.display = 'block'
            }else {
                followingCard[i].style.display = 'none'
            }
        }
    })

    fetch(`/search_followings/${user_instance}`)
    .then(res => res.json())
    .then(data => {
        data.all_user_followings.forEach(d => {
            all_followings.push(d.username)
        })
    })
})