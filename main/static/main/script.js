class Timer {
    constructor(root) {
        this.el = {
            work: $(root).find(".timer__btn--work"),
            break: $(root).find(".timer__btn--break"),
            minutes: $(root).find(".timer__part--minutes"),
            seconds: $(root).find(".timer__part--seconds"),
            control: $(root).find(".timer__btn--control")
        };

        this.w = new Worker("/static/main/timer_worker.js");

        this.w.postMessage({ action: 'firstUpdateTime'})
        this.w.onmessage = this.handleWorkerMessage.bind(this);

        this.el.work.click(() => { 
            this.workTime()
        })

        this.el.break.click(() => {
            this.breakTime()
        })

        this.el.control.click(() => {
            this.control()
        });
    }

    control() {
        requestNotificationPermission();
        const storedSettings = JSON.parse(sessionStorage.getItem('activeBreaksSettings'));
        let auto_start_work_timer = storedSettings[0].auto_start_work_timer;
        let auto_start_break_timer = storedSettings[0].auto_start_break_timer;
        this.w.postMessage({ action: 'control', data: [auto_start_work_timer, auto_start_break_timer]});
    }

    handleWorkerMessage(event) {
        const { action, data = {} } = event.data;

        switch (action) {
            case 'firstUpdateTime':
                this.firstUpdateTime(data);
                break;
            case 'updateInterfaceTime':
                this.updateInterfaceTime(data)
                break;
            case 'updateInterfaceControls':
                this.updateInterfaceControls(data)
                break;
            case 'sendNotification':
                sendNotification(data)
                break;
            case 'workTime':
                this.workTime(data);
                break;
            case 'breakTime':
                this.breakTime(data);
                break;   
          }
        console.log('Messaggio ricevuto dal worker:', event);
    }

    updateTime_afterSettings(newSettings) {
        this.w.postMessage({ action: 'updateTime_afterSettings', data: newSettings})
    }



    workTime(data) {
        const storedSettings = JSON.parse(sessionStorage.getItem('activeBreaksSettings'));
        let remainingSeconds = storedSettings[0].work_duration * 60;

        this.updateInterfaceTime(remainingSeconds)
        this.w.postMessage({ action: 'workTime', data: remainingSeconds});
        if (data) {
            if (data[0] === true) {
                this.w.postMessage({ action: 'control', data: data});
            }
        }
        
    }

    breakTime(data) {
        const storedSettings = JSON.parse(sessionStorage.getItem('activeBreaksSettings'));
        let remainingSeconds = storedSettings[0].break_duration * 60;
        
        this.updateInterfaceTime(remainingSeconds)
        this.w.postMessage({ action: 'breakTime', data: remainingSeconds})
        if (data) {
            if (data[1] === true) {
                this.w.postMessage({ action: 'control', data: data});
            }
        }
        
    }

    firstUpdateTime(data) {
        sessionStorage.setItem('activeBreaksSettings', JSON.stringify(data));
        let remainingSeconds = data[0].work_duration * 60;
        this.updateInterfaceTime(remainingSeconds)
    }

    updateInterfaceTime(data) {
        console.log(data)
        const minutes = Math.floor(data / 60);
        const seconds = data % 60;

        this.el.minutes.text(minutes.toString().padStart(2, "0"));
        this.el.seconds.text(seconds.toString().padStart(2, "0"));
        document.title = "Timer - " + this.el.minutes.text() + ":" + this.el.seconds.text()
        
    }

    updateInterfaceControls(data) {
        if (data === true) {
            audio_btn.play();
            this.el.control.html(`START`);
            this.el.control.addClass("timer__btn--start").removeClass("timer__btn--stop").removeClass('active');
        } else {
            audio_btn2.play();
            this.el.control.html(`STOP`);
            this.el.control.addClass("timer__btn--stop").addClass('active').removeClass("timer__btn--start");
        }
    }

    
    
}


var audio_btn  = new Audio('/static/audios/mouseUp.mp3');
var audio_btn2 = new Audio('/static/audios/mouseDown.mp3')

audio_btn.load();
audio_btn2.load();



function requestNotificationPermission() {
    if ('Notification' in window) {
        Notification.requestPermission().then(function(permission) {
            if (permission === 'granted') {
                console.log('Autorizzazione alle notifiche ottenuta!');
            }
        });
    } else {
        console.error('Questo browser non supporta le notifiche.');
    }
}

function sendNotification(data) {
    if ('Notification' in window && Notification.permission === 'granted') {
        var notification = new Notification(data[0], data[1]);
        playAudio()
    } else {
        console.warn('Le notifiche sono disabilitate o non autorizzate.');
    }
}

function playAudio() {
    new Audio('/static/audios/finish3.wav').play()

}


function getCSRFToken() {
    const name = 'csrftoken=';
    const cookies = document.cookie.split('; ');

    for (let cookie of cookies) {
        if (cookie.startsWith(name)) {
            return cookie.substring(name.length);
        }
    }
    return null;
}