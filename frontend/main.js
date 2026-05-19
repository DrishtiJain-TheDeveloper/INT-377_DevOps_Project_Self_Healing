const API_BASE = 'http://44.247.22.46:30001';

const facts = [
  "The ocean covers more than 70% of Earth's surface but over 80% of it remains unexplored.",
  "The deepest point in the ocean, the Mariana Trench, is about 11,000 meters deep — deeper than Mount Everest is tall.",
  "More than 90% of Earth's living space is in the ocean.",
  "The ocean produces over half of the world's oxygen, mostly from microscopic algae called phytoplankton.",
  "There are more historical artifacts under the sea than in all the world's museums combined.",
  "The blue whale's heart is so large a human could crawl through its arteries.",
  "Some deep-sea fish produce their own light through bioluminescence to attract prey or mates.",
  "The pressure at the bottom of the Mariana Trench is over 1,000 times the standard atmospheric pressure.",
  "Octopuses have three hearts, blue blood, and can change color in milliseconds.",
  "The ocean absorbs about 30% of the CO₂ produced by humans, buffering the effects of climate change."
];

let allSpecies = [];

async function fetchSpecies(zone = 'all') {
  const grid = document.getElementById('species-grid');
  grid.innerHTML = '<p style="color:var(--muted);text-align:center;grid-column:1/-1">Loading...</p>';

  try {
    const url = zone === 'all'
      ? `${API_BASE}/api/species`
      : `${API_BASE}/api/species/${zone}`;

    const res = await fetch(url);
    if (!res.ok) throw new Error('API error');
    const data = await res.json();
    allSpecies = zone === 'all' ? data : allSpecies;
    renderCards(data);
  } catch (err) {
    grid.innerHTML = '<p style="color:#e05c5c;text-align:center;grid-column:1/-1">Failed to load species. Is the backend running?</p>';
  }
}

function renderCards(data) {
  const grid = document.getElementById('species-grid');
  if (data.length === 0) {
    grid.innerHTML = '<p style="color:var(--muted);text-align:center;grid-column:1/-1">No species found.</p>';
    return;
  }
  grid.innerHTML = data.map(s => `
    <div class="species-card" data-id="${s.id}">
      <div class="card-emoji">${s.emoji}</div>
      <div class="card-body">
        <h3>${s.name}</h3>
        <span class="zone-tag">${s.zone_label}</span>
        <p>${s.description.substring(0, 80)}...</p>
      </div>
    </div>
  `).join('');

  document.querySelectorAll('.species-card').forEach(card => {
    card.addEventListener('click', () => {
      const s = (allSpecies.length ? allSpecies : data).find(x => x.id == card.dataset.id);
      if (s) openModal(s);
    });
  });
}

function openModal(s) {
  document.getElementById('modal-img').textContent = s.emoji;
  document.getElementById('modal-name').textContent = s.name;
  document.getElementById('modal-zone').textContent = s.zone_label;
  document.getElementById('modal-desc').textContent = s.description;
  document.getElementById('modal-overlay').classList.add('open');
}

document.getElementById('modal-close').addEventListener('click', () => {
  document.getElementById('modal-overlay').classList.remove('open');
});
document.getElementById('modal-overlay').addEventListener('click', (e) => {
  if (e.target === document.getElementById('modal-overlay'))
    document.getElementById('modal-overlay').classList.remove('open');
});

document.querySelectorAll('.filter-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    fetchSpecies(btn.dataset.filter);
  });
});

document.getElementById('fact-btn').addEventListener('click', () => {
  document.getElementById('fact-text').textContent =
    facts[Math.floor(Math.random() * facts.length)];
});

fetchSpecies();
