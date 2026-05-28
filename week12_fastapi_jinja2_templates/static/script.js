document.addEventListener("click", async (event) => {
  const value = event.target?.dataset?.copy;
  if (!value || !navigator.clipboard) return;
  await navigator.clipboard.writeText(value);
  event.target.dataset.copied = "true";
});
