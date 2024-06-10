
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('[data-toggle="collapse"]').forEach(function(toggleBtn) {
        toggleBtn.addEventListener('click', function() {
            const targetId = toggleBtn.getAttribute('data-target');
            const targetEl = document.querySelector(targetId);
            targetEl.classList.toggle('show');
        });
    });
});