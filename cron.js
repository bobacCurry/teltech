const schedule = require('node-schedule')

var path = require('path')

const child_process = require('child_process')

const fs = require("fs");

const file = path.join(__dirname, './log/cron.log')

const date = new Date()

const day = date.getDate()

const hour = date.getHours()

const minute = date.getMinutes()

const second = date.getSeconds()

const time = hour + ':' + minute + ':' + second

let log = (error) => {

	fs.writeFile(file, time + ':' + error + '\n', { flag: 'a' },(err)=>{
		
		if (err) {

				console.log(err)

			}
		}
	)
}

let work = schedule.scheduleJob('10 */12 * * * *', async () => {
	
	const cmd = 'python3 addChat.py'

	const child = child_process.exec(cmd,{timeout:20000},function (error, stdout, stderr) {
		
		if (error) {

			log('child_error:' + JSON.stringify(error))
		}

		if(stdout){
			
			log('child_stdout: ' + stdout)
		}
	})

	child.on('exit', (code, signal) => {

		log(`exit code ${code} child process exited with signal ${signal}`)
	})
})