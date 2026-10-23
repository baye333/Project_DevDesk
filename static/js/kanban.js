document.addEventListener("DOMContentLoaded", () => {
  const board = document.querySelector(".kanban");
  if (!board) return;
  const csrf = board.dataset.csrf;
  let dragged = null;

  board.querySelectorAll(".kanban-card").forEach((card) => {
    card.addEventListener("dragstart", () => {
      dragged = card;
      card.classList.add("dragging");
    });
    card.addEventListener("dragend", () => {
      card.classList.remove("dragging");
      dragged = null;
    });
  });

  board.querySelectorAll(".kanban-col").forEach((col) => {
    const drop = col.querySelector(".kanban-drop");
    col.addEventListener("dragover", (event) => {
      event.preventDefault();
    });
    col.addEventListener("drop", async (event) => {
      event.preventDefault();
      if (!dragged) return;
      drop.appendChild(dragged);
      const status = col.dataset.status;
      const id = dragged.dataset.id;
      const body = new URLSearchParams({ status });
      const response = await fetch(`/tasks/${id}/status/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": csrf,
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body,
      });
      if (!response.ok) {
        window.location.reload();
      }
    });
  });
});
