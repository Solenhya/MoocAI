//NON FONCTIONNEL

window.addEventListener("DOMContentLoaded", () => {
    const usersContainer = document.getElementById("users");
  
    function displayMessages(users) {
      if (!usersContainer) {
        console.error("usersContainer element not found.");
        return;
      }
      usersContainer.innerHTML = "";
      users.forEach((user, index) => {
        const userRow = document.createElement("div");
        userRow.className = "user-row";
        userRow.id=user._id;
        userRow.textContent = `${index + 1}. ${user.body}`;
        const buttonRow = document.createElement("button");
        buttonRow.id=`button-${message._id}`;
        buttonRow.textContent = `Voir`;
        buttonRow.addEventListener("click", () => {
        window.location.href = `/user/${message._id}`;
          });
        messageRow.append(buttonRow);
        messagesContainer.appendChild(messageRow);
      });
    }
  
    // Expose displayMessages globally
    window.displayMessages = displayMessages;
  });