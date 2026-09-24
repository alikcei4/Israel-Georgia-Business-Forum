// Language pages share section IDs, so keep the current section when switching.
function updateLanguageLinks() {
  document.querySelectorAll('.language-link').forEach(link => {
    const destination = new URL(link.getAttribute('href'), location.href);
    destination.hash = location.hash;
    link.href = destination.href;
  });
}
updateLanguageLinks();
window.addEventListener('hashchange', updateLanguageLinks);
