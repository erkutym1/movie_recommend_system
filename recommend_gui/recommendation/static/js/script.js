document.addEventListener("DOMContentLoaded", function () {
    const filterToggle = document.getElementById("filter");
    const userIdInput = document.getElementById("userId");
    const genreSelect = document.getElementById("genre");
    const recommendButton = document.querySelector(".btn");
    const recommendationOutput = document.querySelector(".input");

    // Toggle the visibility of the userId input based on the filter
    filterToggle.addEventListener("change", function () {
        if (filterToggle.checked) {
            // Personal Recommendation mode
            userIdInput.style.display = "none";
        } else {
            // Popular Recommendations mode
            userIdInput.style.display = "block";
        }
    });

    recommendButton.addEventListener("click", function () {
        const userId = userIdInput.value;
        const selectedGenre = genreSelect.value;

        // Check if userId is a valid number
        if (!filterToggle.checked && (!/^\d+$/.test(userId) || userId === "")) {
            recommendationOutput.value = "USER ID HATALI";
            return;
        }

        // Check if a genre is selected
        if (selectedGenre === "") {
            recommendationOutput.value = "KATEGORİ SEÇİLMEDİ";
            return;
        }

        if (filterToggle.checked) {
            // Fetch the top movies CSV file for Popular Recommendations
            fetch('/media/process3_top15_movies_by_genre.csv')
                .then(response => {
                    if (!response.ok) {
                        throw new Error('File not found');
                    }
                    return response.text();
                })
                .then(data => {
                    const rows = data.split('\n').slice(1); // Ignore header
                    const filteredMovies = rows.filter(row => {
                        const columns = row.split(',');
                        return columns[0].trim() === selectedGenre; // Check genre match
                    });

                    if (filteredMovies.length > 0) {
                        const randomMovie = filteredMovies[Math.floor(Math.random() * filteredMovies.length)];
                        const movieDetails = randomMovie.split(',');
                        recommendationOutput.value = movieDetails[1].trim(); // Set the movie name
                    } else {
                        recommendationOutput.value = "Bu kategoride öneri yok.";
                    }
                })
                .catch(error => {
                    console.error('Error fetching the top movies file:', error);
                    recommendationOutput.value = "Bir hata oluştu.";
                });
        } else {
            // Fetch the corresponding recommendation CSV file for Personal Recommendations
            fetch(`/media/process9/user_${userId}_recommend_scores.csv`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('File not found');
                    }
                    return response.text();
                })
                .then(data => {
                    const rows = data.split('\n').slice(1); // Ignore header
                    const filteredMovies = rows.filter(row => {
                        const columns = row.split(',');
                        return columns[0].trim() === selectedGenre; // Check genre match
                    });

                    if (filteredMovies.length > 0) {
                        const randomMovie = filteredMovies[Math.floor(Math.random() * filteredMovies.length)];
                        const movieDetails = randomMovie.split(',');
                        recommendationOutput.value = movieDetails[1].trim(); // Set the movie name
                    } else {
                        recommendationOutput.value = "Bu kategoride öneri yok.";
                    }
                })
                .catch(error => {
                    console.error('Error fetching the recommendation file:', error);
                    recommendationOutput.value = "Bir hata oluştu.";
                });
        }
    });
});
