import React from 'react';

const ActionProvider = ({ createChatBotMessage, setState, children }) => {
    const handleHello = (message) => {
        // Fetch the data from your endpoint
        console.log("message: " + message)
        fetch(`http://127.0.0.1:5000/temu/chat?query=${encodeURIComponent(message)}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to load data');
            }
            let text = response.json()
            console.log("text" + text)
            return text;
        })
        .then(data => {
            // Create a chatbot message with the response data
            const botMessage = createChatBotMessage(data); // Assuming data.message contains the response message
            // Update the chatbot state to include the new message
            let data2 = data
            console.log("data2" + data2)
            setState(prev => ({
                ...prev,
                messages: [...prev.messages, botMessage],
            }));
        })
        .catch(error => {
            console.error("Error fetching data", error);
            // Optionally handle the error by sending a user-friendly message
            const errorMessage = createChatBotMessage("Sorry, there was an error processing your request.");
            setState(prev => ({
                ...prev,
                messages: [...prev.messages, errorMessage],
            }));
        });
    };

    // Wrap children with action properties
    return (
        <div>
            {React.Children.map(children, child => {
                return React.cloneElement(child, {
                    actions: {
                        handleHello,
                    },
                });
            })}
        </div>
    );
};

export default ActionProvider;
