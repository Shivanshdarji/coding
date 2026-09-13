
const revealButton = document.getElementById('reveal-button');
const birthdayMessage = document.getElementById('birthday-message');
const birthdayButton = document.getElementById('birthday-button');
const candlesDiv = document.getElementById('candles');
const messageContainer = document.getElementById('message-container');
const messageInput = document.getElementById('message-input');
const saveMessageButton = document.getElementById('save-message-button');
const savedMessagesDiv = document.getElementById('saved-messages');
const previousMessagesDiv = document.getElementById('previous-messages');

const photos = document.querySelectorAll('.sister-photo');
const storyContainer = document.getElementById('photo-story');

photos.forEach((photo) => {
  photo.addEventListener('click', () => {
    const story = photo.getAttribute('data-story');
    storyContainer.innerHTML = story;
    storyContainer.style.display = 'block';
  });
});

photos.forEach((photo) => {
photo.addEventListener('click', () => {
const story = photo.getAttribute('data-story');
photoStoryContainer.innerHTML = story;
photoStoryContainer.style.display = 'block';
});
});
function showStory(story) {
    document.getElementById('photo-story').innerHTML = story;
    document.getElementById('photo-story').style.display = 'block';
}
         
revealButton.addEventListener('click', () => {
    birthdayMessage.style.display = 'block';
    revealButton.style.display = 'none';
});

birthdayButton.addEventListener('click', () => {
    candlesDiv.innerHTML = '';
    for (let i = 0; i < 10; i++) {
        const candle = document.createElement('div');
        candle.classList.add('candle');
        candlesDiv.appendChild(candle);
        setTimeout(() => {
            candle.classList.add('flame');
        }, Math.random() * 2000);
    }
    messageContainer.style.display = 'block';
});

saveMessageButton.addEventListener('click', () => {
    const message = messageInput.value;
    if (message !== '') {
        const savedMessages = localStorage.getItem('savedMessages');
        if (savedMessages === null) {
            localStorage.setItem('savedMessages', JSON.stringify([message]));
        } else {
            const messagesArray = JSON.parse(savedMessages);
            messagesArray.push(message);
            localStorage.setItem('savedMessages', JSON.stringify(messagesArray));
        }
        messageInput.value = '';
        displaySavedMessages();
        displayPreviousMessages();
        sendEmail();
    }
});

function displaySavedMessages() {
    const savedMessages = localStorage.getItem('savedMessages');
    if (savedMessages !== null) {
        const messagesArray = JSON.parse(savedMessages);
        savedMessagesDiv.innerHTML = '';
        messagesArray.forEach((message) => {
            const savedMessage = document.createElement('p');
            savedMessage.textContent = message;
            savedMessagesDiv.appendChild(savedMessage);
        });
    }
}

function displayPreviousMessages() {
    const savedMessages = localStorage.getItem('savedMessages');
    if (savedMessages !== null) {
        const messagesArray = JSON.parse(savedMessages);
        previousMessagesDiv.innerHTML = '';
        messagesArray.forEach((message, index) => {
            const previousMessage = document.createElement('div');
            previousMessage.innerHTML = `
                <p>${message}</p>
                <button class="delete-button" data-index="${index}">Delete</button>
            `;
            previousMessagesDiv.appendChild(previousMessage);
        });
        const deleteButtons = document.querySelectorAll('.delete-button');
        deleteButtons.forEach((button) => {
            button.addEventListener('click', () => {
                const index = button.getAttribute('data-index');
                const savedMessages = localStorage.getItem('savedMessages');
                if (savedMessages !== null) {
                    const messagesArray = JSON.parse(savedMessages);
                    messagesArray.splice(index, 1);
                    localStorage.setItem('savedMessages', JSON.stringify(messagesArray));
                    displayPreviousMessages();
                }
            });
        });
    }
}

function sendEmail() {
    const savedMessages = localStorage.getItem('savedMessages');
    if (savedMessages !== null) {
        const messagesArray = JSON.parse(savedMessages);
        const emailServiceId = 'YOUR_EMAILJS_SERVICE_ID';
        const emailTemplateId = 'YOUR_EMAILJS_TEMPLATE_ID';
        const userId = 'YOUR_EMAILJS_USER_ID';
        emailjs.send(emailServiceId, emailTemplateId, {
            messages: messagesArray.join('\n'),
            to_email: 'shivanshdarji56@gmail.com',
        }, userId)
        .then((response) => {
            console.log('Email sent successfully:', response);
        })
        .catch((error) => {
            console.error('Error sending email:', error);
        });
    }
}
