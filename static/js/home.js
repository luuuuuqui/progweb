document.addEventListener('DOMContentLoaded', function() {
    const favoriteButtons = document.querySelectorAll('.btn-favorite');
    
    // Get favorites list from localStorage
    let favorites = JSON.parse(localStorage.getItem('favorited_products')) || [];
    
    // Update button states on load
    favoriteButtons.forEach(button => {
        const prodId = button.getAttribute('data-id');
        if (favorites.includes(prodId)) {
            setAsFavorited(button);
        }
    });

    // Handle clicks
    favoriteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const prodId = this.getAttribute('data-id');
            let favorites = JSON.parse(localStorage.getItem('favorited_products')) || [];
            
            if (favorites.includes(prodId)) {
                // Remove from favorites
                favorites = favorites.filter(id => id !== prodId);
                setAsNotFavorited(this);
            } else {
                // Add to favorites
                favorites.push(prodId);
                setAsFavorited(this);
                // Add a small scale animation
                this.style.transform = 'scale(1.15)';
                setTimeout(() => {
                    this.style.transform = 'none';
                }, 150);
            }
            
            localStorage.setItem('favorited_products', JSON.stringify(favorites));
        });
    });

    function setAsFavorited(btn) {
        btn.classList.remove('btn-warning');
        btn.classList.add('btn-danger');
        const textSpan = btn.querySelector('.fav-text');
        if (textSpan) textSpan.textContent = 'Favoritado';
        btn.style.backgroundColor = '#dc3545';
        btn.style.borderColor = '#dc3545';
        btn.style.color = '#ffffff';
        btn.style.transition = 'transform 0.15s ease-in-out, background-color 0.2s';
    }

    function setAsNotFavorited(btn) {
        btn.classList.remove('btn-danger');
        btn.classList.add('btn-warning');
        const textSpan = btn.querySelector('.fav-text');
        if (textSpan) textSpan.textContent = 'Favoritar';
        btn.style.backgroundColor = '#ffc107';
        btn.style.borderColor = '#ffc107';
        btn.style.color = '#212529';
    }
});
