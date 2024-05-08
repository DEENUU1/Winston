function storeConversationName(button) {
    var conversationName = button.getAttribute('data-conversation-name');
    console.log('Conversation Name:', conversationName);
    document.getElementById('conversation_name').value = conversationName;
    document.getElementById('conversationForm').setAttribute('hx-post', '/conversation/' + conversationName);
    htmx.process(document)
}