document.addEventListener('DOMContentLoaded', () => {

    const dropdownBtn = document.querySelector('.user-dropdown-btn')
    const userDropdownContent = document.querySelector('.user-dropdown-content')

    if(userDropdownContent != null){
        userDropdownContent.style.display = 'none'
    }
    if(dropdownBtn != null){
        dropdownBtn.onclick = () => {
            if(userDropdownContent.style.display === 'block'){
                userDropdownContent.style.display = 'none'
            } else {
                userDropdownContent.style.display = 'block'
            }
        }
    }
    window.addEventListener('mouseup', function(event) {
        if(event.target != userDropdownContent && event.target.parentNode != dropdownBtn){
           if(userDropdownContent != null){
            userDropdownContent.style.display = 'none'
           }
        }
    })
    const activeLink = window.location.pathname;
    const homeLink = document.querySelector('#home-link')
    const navbarLinks = document.querySelectorAll('.navbar-links ul li a').forEach(link => {
        if(activeLink === '/'){
            homeLink.classList.add('active');
        } else if (link.href.includes(`${activeLink}`)){
            link.classList.add('active')
        }
    })
})