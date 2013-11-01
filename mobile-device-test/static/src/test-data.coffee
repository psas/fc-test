
mesgbox = document.getElementById("mesg")
accelbox = document.getElementById("moAccel")

proxy = (fn, context) ->
    p = -> fn.apply(context)
    return p

class Motion

    constructor: ->

    deviceMotionHandler: (evt) ->
        accel = evt.accelerationIncludingGravity
        message = '['+accel.x+','+accel.y+','+accel.z+']'
        accelbox.innerHTML = message
        conn.send(message)
        return


class Connection

    constructor: ->
        @websocket = new WebSocket 'ws://'+ location.host + '/ws'
        @websocket.onopen = (evt) => mesgbox.innerHTML += "<br>Open Socket"
        @websocket.onclose = (evt) =>
            mesgbox.innerHTML +=  "<br>Close Socket"
            return
        @websocket.onerror = (evt) =>
            mesgbox.innerHTML += '<br>ERROR'+evt
            return
        @websocket.onmessage = (evt) =>

    send: (msg) ->
        if @websocket? and @websocket.readyState is WebSocket.OPEN
            @websocket.send(msg)
        return


conn = new Connection()


if window.DeviceMotionEvent
    mesgbox.innerHTML = "Your device is supported"
    motion = new Motion()
    #setTimeout (-> motion.deviceMotionHandler("adsf")), 1000
    window.addEventListener('devicemotion', motion.deviceMotionHandler, false)
else
    mesgbox.innerHTML = "Your device is not supported. :("
