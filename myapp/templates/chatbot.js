var message_container = document.getElementById('message-container')
        
        // Function to send message via AJAX
        function sendMessage() {
            var question = $('#message-input').val();
            var p = document.createElement("p");
            p.textContent = question
            message_container.appendChild(p)
            
            p = document.createElement("pre");
            p.textContent = "Thinking..."
            message_container.appendChild(p)

            $.ajax({
                url: '/response',
                type: 'POST',
                data: {
                    'user_input': question
                },
                headers: { "X-CSRFToken": '{{csrf_token}}' },
                success: function(response) {
                    // Do something with the response if needed
                    $('#message-container').val(response)
                    p.textContent = response
                },
                error: function(error) {
                    console.error('Error:', error);
                }
            });
            // Clear the input field after sending message
            $('#message-input').val('');
        }

    // Event listener for send button
    $('#send-button').click(function() {
        sendMessage();
    });

    // Optionally, you can also send message when Enter key is pressed
    $('#message-input').keypress(function(event) {
        if (event.which == 13) {
            sendMessage();
        }
    });