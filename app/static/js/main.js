// MediAsk — Client-side interactions

// Vote handler with animation
function vote(answerId, value) {
    const csrfToken = document.querySelector('[name=csrf_token]')?.value
        || document.querySelector('meta[name="csrf-token"]')?.content
        || (typeof window.csrfToken !== 'undefined' ? window.csrfToken : '');

    const controls = document.querySelector(`[data-answer-id="${answerId}"]`);
    const scoreEl = controls?.querySelector('.vote-score');

    fetch('/questions/vote', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ answer_id: answerId, value: value })
    })
    .then(r => {
        if (!r.ok) {
            if (r.status === 401) {
                window.location.href = '/auth/login';
                return;
            }
            throw new Error('Vote failed');
        }
        return r.json();
    })
    .then(data => {
        if (data && data.score !== undefined && scoreEl) {
            scoreEl.textContent = data.score;
            scoreEl.style.transform = 'scale(1.3)';
            setTimeout(() => scoreEl.style.transform = 'scale(1)', 200);
        }
    })
    .catch(err => console.error('Vote error:', err));
}

// Make question cards clickable
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.question-card').forEach(card => {
        const link = card.querySelector('h3 a');
        if (link) {
            card.addEventListener('click', (e) => {
                if (e.target.tagName !== 'A') {
                    window.location.href = link.href;
                }
            });
        }
    });
});
