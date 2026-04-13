document.addEventListener('DOMContentLoaded', () => {
    const searchForm = document.getElementById('search-form');
    const movieInput = document.getElementById('movie-input');
    const loadingState = document.getElementById('loading-state');
    const errorState = document.getElementById('error-state');
    const resultsSection = document.getElementById('results-section');
    const movieGrid = document.getElementById('movie-grid');

    window.submitForm = async function() {
        const title = movieInput.value.trim();
        if (!title) return;

        // Reset UI
        errorState.classList.add('hidden');
        resultsSection.classList.add('hidden');
        loadingState.classList.remove('hidden');
        movieGrid.innerHTML = '';

        try {
            const response = await fetch('/api/recommend', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ title })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Failed to fetch recommendations.');
            }

            renderMovies(data.recommendations);
            
            loadingState.classList.add('hidden');
            resultsSection.classList.remove('hidden');

            // Stagger animation for cards
            const cards = document.querySelectorAll('.movie-card');
            cards.forEach((card, index) => {
                setTimeout(() => {
                    card.style.opacity = '1';
                    card.style.transform = 'translateY(0)';
                }, index * 100);
            });

        } catch (error) {
            loadingState.classList.add('hidden');
            errorState.textContent = "* Error: " + error.message;
            errorState.classList.remove('hidden');
        }
    };

    searchForm.addEventListener('submit', (e) => {
        e.preventDefault();
        window.submitForm();
    });

    function renderMovies(movies) {
        movieGrid.innerHTML = movies.map(movie => `
            <article class="movie-card">
                <h3>${movie.title}</h3>
                <div class="movie-meta">
                    <span class="rating">⭐ ${parseFloat(movie.vote_average || 0).toFixed(1)}/10</span>
                    <span class="year">${movie.release_date ? movie.release_date.split('-')[0] : 'N/A'}</span>
                </div>
                <p class="movie-overview">${movie.overview || 'No overview available.'}</p>
            </article>
        `).join('');
    }
});
