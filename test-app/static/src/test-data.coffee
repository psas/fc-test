# placeholders for putting message in the client
mesgbox = document.getElementById("mesg")
accelbox = document.getElementById("moAccel")

# this is dumb, but somehow it's not built into javascript
round = (v) -> Math.round(v*100.0)/100.0

# Very basic websocket class
class Connection

    constructor: ->
        @websocket = new WebSocket 'ws://'+ location.host + '/ws'
        @websocket.onopen = (evt) => mesgbox.innerHTML += "<br>websocket open"
        @websocket.onclose = (evt) => mesgbox.innerHTML +=  "<br>websocket closed"
        @websocket.onerror = (evt) => mesgbox.innerHTML += '<br>ERROR'+evt
        @websocket.onmessage = (evt) =>

    send: (msg) ->
        if @websocket? and @websocket.readyState is WebSocket.OPEN
            @websocket.send(msg)
        return

# Motion data handler
deviceMotionHandler = (evt) ->

        # Read data
        accel    = evt.accelerationIncludingGravity
        rot      = evt.rotationRate
        interval = evt.interval

        # Show in screen
        message = 'Accel: ['+round(accel.x)+', '+round(accel.y)+', '+round(accel.z)+'] at rate '+1/(interval/1000.0)+' Hz'
        accelbox.innerHTML = message

        # pack for delivery
        data =
            acc:
                x: accel.x
                y: accel.y
                z: accel.z
            rate: interval

        # send data
        conn.send JSON.stringify data
        return

# Create connection
conn = new Connection()

# Check if we're on a compatible device
if window.DeviceMotionEvent
    mesgbox.innerHTML = "Your device is supported"
    # Attach the event here
    window.addEventListener('devicemotion', deviceMotionHandler, false)
else
    mesgbox.innerHTML = "Your device is not supported. :("
