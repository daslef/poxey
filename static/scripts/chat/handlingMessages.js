var socket = io.connect(`http://${document.domain}:${location.port}`);     
const chat = document.getElementsByClassName("chat-content")[0];

chat.scrollTop = chat.scrollHeight;

socket.on("connect", () => {
    $("form").on("submit", (e) => {
        e.preventDefault();
        let user = $("#username").text();
        let msg = $(".user-message").val();

        socket.emit("userMessage", {
            username: user,
            message: msg
        });
        
        $(".user-message").val("").focus();
    });
});

socket.on("messageResponse", (msg) => {
    const { username, message, time } = msg;
    if(typeof username !== "undefined") {
        $(".chat-content").append(`<div class="chat-content__row">
                                        <div class="row-left">
                                            <p class="row-username">${username}</p>
                                            <p class="row-usermessage">${message}</p>
                                        </div>
                                        <div>
                                            <p>${time}</p>
                                        </div>
                                    </div>`);
    }
    
    chat.scrollTop = chat.scrollHeight;
});