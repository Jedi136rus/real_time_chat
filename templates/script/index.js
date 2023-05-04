// установка SSE соединения
const source = new EventSource("{{ url_for('sse.stream') }}");

  source.addEventListener('bigboxcode', function (currentEvent) {
    if (currentEvent.data.length > 0) {
      const listElement = document.getElementById('list');
      const newElement = document.createElement('li');
      newElement.innerText = currentEvent.data;

      listElement.appendChild(newElement);

      console.log(JSON.parse(event.data));
    }
  }, false);

  source.addEventListener('error', function (currentEvent) {
    console.log(currentEvent)
  }, false);

// логика отправки сообщения
function init() {
    var sendButton = document.getElementById("sendMessage");
    sendButton.onclick = sendMessage;       // sendMes ф-я отправки сообщения эвент нажатия кнопки
    var sendInput = document.getElementById("messageInput");
    sendInput.onkeypress = sendMessageEntr;
}

// функция отправки сообщения на сервер
async function sendMessage() {
    var sendInput = document.getElementById("messageInput"); // считывание значения поля ввода
    var text = sendInput.value;
    var data = {
        user_id: '{{ user_id }}',
        text: text
    }

    const url = "{{ url_for('/publish') }}";
    try {
        const response = await fetch(url, {
            method: 'POST', // или 'PUT'
            body: JSON.stringify(data), // данные могут быть 'строкой' или {объектом}!
            headers: {
                'Content-Type': 'application/json'
            }
        });
        const json = await response.json();
        console.log('Успех:', JSON.stringify(json));
    } catch (error) {
        console.error('Ошибка:', error);
    }
}
function sendMessageEntr(e) {
      var sendButton = document.getElementById("sendMessage");
      if(e.keyCode === 13) {
            sendButton.click();
            return false;
        }
}

window.onload = init;