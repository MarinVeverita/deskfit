
class TimerWorker {
    constructor() {
        this.interval = null;
        this.remainingSeconds = 0;
        this.current_interval = 'work';

        self.onmessage = this.handleWorkerMessage.bind(this);

        
        
    }


    handleWorkerMessage(event) {
        const { action, data = {} } = event.data;

        switch (action) {
            case 'firstUpdateTime':
                this.firstUpdateTime();
                break;
            case 'workTime':
                this.workTime(data);
                break;
            case 'breakTime':
                this.breakTime(data);
                break
            case 'control':
                this.control(data);
                break
            case 'updateTime_afterSettings':
                this.updateTime_afterSettings(data);
                break
          }
    }

    updateTime_afterSettings(data) {
        switch (this.current_interval) {
            case 'break':
                this.breakTime(data[0].break_duration * 60)
                break
                
            case 'work':
                this.workTime(data[0].work_duration * 60)
        }
        self.postMessage({ action: 'updateInterfaceTime', data: this.remainingSeconds});
    }

    firstUpdateTime() {
        fetch('/api/active-breaks-settings/')
        .then(response => response.json())
        .then(data => {
            this.remainingSeconds = data[0].work_duration * 60;
            this.current_interval = 'work';
            self.postMessage({ action: 'firstUpdateTime', data: data});
        });
    }


    workTime(data) {
        if (this.interval !== null) {
                this.stop();
            }
            
            this.remainingSeconds = data
            this.current_interval = 'work';
    }


    breakTime(data) {
        if (this.interval !== null) {
                this.stop();
            }
            this.remainingSeconds = data
            this.current_interval = 'break';
    }


    control(data) {
        if (this.interval === null) {
            this.start(data);
        } else {
            this.stop();
        }
    };


    

    start(data) {
        if (this.remainingSeconds === 0) return;
        

        this.interval = setInterval(() => {
            this.remainingSeconds--;
            self.postMessage({ action: 'updateInterfaceTime', data: this.remainingSeconds});


            if (this.remainingSeconds === 0) {
                switch (this.current_interval) {
                    case 'break':
                        self.postMessage({ action: 'sendNotification', data: ['Time to work!', { icon: '/static/images/logo.png' }]});
                        break
                    case 'work':
                        self.postMessage({ action: 'sendNotification', data: ['Time for a short break!', { icon: '/static/images/logo.png' }]});
                }
                

                this.stop();

                switch (this.current_interval) {
                    case 'break':
                        if (data[0] === true) {
                            self.postMessage({ action: 'workTime', data: data});
                        } else {
                            self.postMessage({ action: 'workTime'});
                        }
                    
                        break
                        
                    case 'work':
                        if (data[1] === true) {
                            self.postMessage({ action: 'breakTime', data: data})
                        } else {
                            self.postMessage({ action: 'breakTime'})
                        }
                }
            }
        }, 1000);

        const is_interval_present = false;
        self.postMessage({ action: 'updateInterfaceControls', data: is_interval_present});
    }

    stop() {
        clearInterval(this.interval);

        this.interval = null;

        const is_interval_present = true;
        self.postMessage({ action: 'updateInterfaceControls', data: is_interval_present});
    }

    
}




  const timerWorker = new TimerWorker();