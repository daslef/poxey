var socket = io.connect(`http://${document.domain}:${location.port}`);
        
chat = document.getElementsByClassName("chat-content")[0];
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
    if(typeof msg.username !== "undefined") {
        $(".chat-content").append(`<div class="chat-content__row">
                                    <div class="row-left">
                                        <p class="row-username">${msg.username}</p>
                                        <p class="row-usermessage">${msg.message}</p>
                                    </div>
                                    <div>
                                        <p>${msg.time}</p> 
                                    </div>
                                </div>`);
    }
    
    chat = document.getElementsByClassName("chat-content")[0];
    chat.scrollTop = chat.scrollHeight;
});