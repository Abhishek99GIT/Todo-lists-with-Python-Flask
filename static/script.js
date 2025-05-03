
        // Load saved theme from localStorage
        const themeToggle = document.getElementById('themeToggle');
        const htmlElement = document.documentElement;
        const savedTheme = localStorage.getItem('theme') || 'light';
        
        if (savedTheme === 'dark') {
            htmlElement.setAttribute('data-bs-theme', 'dark');
            themeToggle.checked = true;
        }

        // Toggle theme on switch change
        themeToggle.addEventListener('change', () => {
            if (themeToggle.checked) {
                htmlElement.setAttribute('data-bs-theme', 'dark');
                localStorage.setItem('theme', 'dark');
            } else {
                htmlElement.setAttribute('data-bs-theme', 'light');
                localStorage.setItem('theme', 'light');
            }
        });

        
  