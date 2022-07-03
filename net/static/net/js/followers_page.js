document.addEventListener('DOMContentLoaded', () => {
    const followerSearch = document.querySelector('.followers-search')
    const followerCard = document.querySelectorAll('.followers-card')
    const userInstance = JSON.parse(document.getElementById('userInstance').textContent)
    all_followers = []

    followerSearch.addEventListener('input', e => {
        const val = e.target.value.toLowerCase();
        for(i=0; i < all_followers.length; i++){
            if(all_followers[i].includes(val)){
                followerCard[i].style.display = 'block'
            }else {
                followerCard[i].style.display = 'none'
            }
        }
    })

    fetch(`/search_followers/${userInstance}`)
    .then(res => res.json())
    .then(data => {
        data.all_user_followers.forEach(d => {
            all_followers.push(d.username)
            console.log(all_followers)
        })
    })
})