class Chatbox {
    /**
     * Constructor: Inicializa propiedades para elementos DOM, estado del chat, mensajes, contexto y detección de imagen.
     */
    constructor() {
        this.elements = {
            openButton: document.querySelector('.chatbox__button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button')
        };

        this.state = false;
        this.messages = [];
        this.context = '';
        this.image = false;
    }

    /**
     * Muestra el chatbox y configura los eventos para enviar mensajes.
     */
    display() {
        const { openButton, chatBox, sendButton } = this.elements;

        // Detecta si hay una imagen cargada en la página
        const imagenCargada = document.querySelector('.imagen_estadistica');
        this.image = !!imagenCargada;

        openButton.addEventListener('click', () => this.toggleState(chatBox));
        sendButton.addEventListener('click', () => this.onSendButton(chatBox));

        const node = chatBox.querySelector('input');
        node.addEventListener("keyup", ({ key }) => {
            if (key === "Enter") {
                this.onSendButton(chatBox);
            }
        });
    }

    /**
     * Alterna la visibilidad del chatbox.
     * @param {HTMLElement} chatBox Elemento del DOM del chatbox.
     */
    toggleState(chatBox) {
        this.state = !this.state;

        // Muestra u oculta el chatbox
        chatBox.classList.toggle('chatbox--active', this.state);
    }

    /**
     * Envia un mensaje al chatbot y actualiza la interfaz con la respuesta.
     * @param {HTMLElement} chatBox Elemento del DOM del chatbox.
     */
    onSendButton(chatbox) {
        var textField = chatbox.querySelector('input');
        let text1 = textField.value
        if (text1 === "") {
            return;
        }
    
        let userMessage = { name: "User", message: text1 };
        this.messages.push(userMessage);
    
        const endpoint = this.image ? '/predict1' : '/predict';
    
        fetch(endpoint, {
            method: 'POST',
            body: JSON.stringify({ message: text1 }),
            mode: 'cors',
            headers:{
                'Content-Type': 'application/json'
            },
        })
        .then(r => r.json())
        .then(r => {
            let responseMessage = { name: "David", message: r.answer };
            this.messages.push(responseMessage);
            console.log(responseMessage);
            this.updateChatText(chatbox);
            textField.value = '';
        })
        .catch((error) => {
            console.error('Error:', error);
            this.updateChatText(chatbox);
            textField.value = '';
        });
    }
    
    /**
     * Actualiza el contenido del chatbox con los mensajes.
     * @param {HTMLElement} chatBox Elemento del DOM del chatbox.
     */
    updateChatText(chatbox) {
        var html = '';
        this.messages.slice().reverse().forEach(function(item,index) {
            if (item.name === "David") {
                html += '<div class="messages__item messages__item--visitor">' + item.message + '</div>'
            } 
            else {
                html += '<div class="messages__item messages__item--operator">' + item.message + '</div>'
            }
        });

        const chatmessage = chatbox.querySelector('.chatbox__messages');
        chatmessage.innerHTML = html;
    }
}

const chatbox = new Chatbox();
chatbox.display();
