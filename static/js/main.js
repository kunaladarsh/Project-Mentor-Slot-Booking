// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Add fade-in animation to elements
    const fadeElements = document.querySelectorAll('.fade-in');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    });

    fadeElements.forEach(element => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        element.style.transition = 'all 0.5s ease-out';
        observer.observe(element);
    });

    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Dynamic slot availability check
    const slotCards = document.querySelectorAll('.slot-card');
    slotCards.forEach(card => {
        card.addEventListener('click', function() {
            if (this.classList.contains('available')) {
                this.classList.toggle('selected');
            }
        });
    });

    // Date picker enhancement
    const dateInputs = document.querySelectorAll('input[type="date"]');
    dateInputs.forEach(input => {
        input.addEventListener('change', function() {
            const selectedDate = new Date(this.value);
            const today = new Date();
            if (selectedDate < today) {
                this.setCustomValidity('Please select a future date');
            } else {
                this.setCustomValidity('');
            }
        });
    });

    // Time slot validation
    const timeInputs = document.querySelectorAll('input[type="time"]');
    timeInputs.forEach(input => {
        input.addEventListener('change', function() {
            const startTime = document.querySelector('input[name="start_time"]');
            const endTime = document.querySelector('input[name="end_time"]');
            
            if (startTime && endTime) {
                const start = new Date(`1970-01-01T${startTime.value}`);
                const end = new Date(`1970-01-01T${endTime.value}`);
                
                if (end <= start) {
                    endTime.setCustomValidity('End time must be after start time');
                } else {
                    endTime.setCustomValidity('');
                }
            }
        });
    });

    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Responsive table enhancement
    const tables = document.querySelectorAll('.table-responsive');
    tables.forEach(table => {
        table.addEventListener('scroll', function() {
            const scrollLeft = this.scrollLeft;
            const scrollWidth = this.scrollWidth;
            const clientWidth = this.clientWidth;
            
            if (scrollLeft > 0) {
                this.classList.add('scrolled-left');
            } else {
                this.classList.remove('scrolled-left');
            }
            
            if (scrollLeft + clientWidth < scrollWidth) {
                this.classList.add('scrolled-right');
            } else {
                this.classList.remove('scrolled-right');
            }
        });
    });

    // Search functionality for tables
    const searchInputs = document.querySelectorAll('.table-search');
    searchInputs.forEach(input => {
        input.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const table = this.closest('.card').querySelector('table');
            const rows = table.querySelectorAll('tbody tr');
            
            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(searchTerm) ? '' : 'none';
            });
        });
    });

    // Profile image preview
    const imageInput = document.querySelector('input[type="file"][accept="image/*"]');
    if (imageInput) {
        imageInput.addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    const preview = document.querySelector('.profile-image-preview');
                    if (preview) {
                        preview.src = e.target.result;
                    }
                };
                reader.readAsDataURL(file);
            }
        });
    }
}); 