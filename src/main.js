// ---------- Menu overlay ----------
const menuBtn = document.getElementById('menu-btn');
const overlay = document.getElementById('menu-overlay');

function toggleMenu(open) {
  overlay.classList.toggle('open', open);
  menuBtn.setAttribute('aria-expanded', String(open));
  document.body.style.overflow = open ? 'hidden' : '';
}

menuBtn.addEventListener('click', () => toggleMenu(!overlay.classList.contains('open')));

overlay.querySelectorAll('a[href^="#"]').forEach((a) =>
  a.addEventListener('click', () => toggleMenu(false))
);

document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') toggleMenu(false);
});

// ---------- Reveal on scroll ----------
const io = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        io.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.12 }
);
document.querySelectorAll('.reveal').forEach((el) => io.observe(el));

// ---------- Project card click -> subtle press feedback ----------
document.querySelectorAll('.project-card').forEach((card) => {
  card.addEventListener('click', () => {
    card.animate(
      [
        { transform: 'translateY(0)' },
        { transform: 'translateY(-6px)' },
        { transform: 'translateY(0)' },
      ],
      { duration: 450, easing: 'cubic-bezier(0.16, 1, 0.3, 1)' }
    );
  });
});
