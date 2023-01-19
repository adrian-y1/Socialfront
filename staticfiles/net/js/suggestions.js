document.addEventListener('DOMContentLoaded', () => {
    const suggestionSearch = document.querySelector('.suggestion-search')
    const suggestionCard = document.querySelectorAll('.suggestion-card')

    all_suggestions = []

    suggestionSearch.addEventListener('input', e => {
        const val = e.target.value.toLowerCase();
        for(i=0; i < all_suggestions.length; i++){
            if(all_suggestions[i].includes(val)){
                suggestionCard[i].style.display = 'block'
            }else {
                suggestionCard[i].style.display = 'none'
            }
        }
    })

    fetch(`/suggestions_api`)
    .then(res => res.json())
    .then(data => {
        data.forEach(d => {
            all_suggestions.push(d.username)
        })
    })
})