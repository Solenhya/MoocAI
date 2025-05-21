window.addEventListener("DOMContentLoaded", () => {
    const messagesContainer = document.getElementById("messages");
  
    function displayMessages(messages) {
      if (!messagesContainer) {
        console.error("messagesContainer element not found.");
        return;
      }
      messagesContainer.innerHTML = "";
      messages.forEach((message, index) => {
        const messageRow = document.createElement("div");
        messageRow.className = "message-row";
        messageRow.id=message._id;
        messageRow.textContent = `${index + 1}. ${message.body}`;
        messagesContainer.appendChild(messageRow);
        const buttonRow = document.createElement("button");
        buttonRow.id=`button-${message._id}`;
        buttonRow.textContent = `Voir`;
        messageRow.append(buttonRow);
      });
    }
  
    // Expose displayMessages globally
    window.displayMessages = displayMessages;
  });