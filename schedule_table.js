var ScheduleTable = function(height, width) {
	this.height = height;
	this.width = width;
	this.days = new Array(this.width);
    // make an empty checkerboard
    for (var i=0; i < this.width; i++){
		this.days[i] = [];
	}
	
	this.paint = function(day, hour, color) {
		if (this.days[day][hour] == color) {
			delete this.days[day][hour];
			this.dispatchEvent("paint", {day:day, hour:hour, newColor:"blank"});
		} else {
			this.days[day][hour] = color;
			this.dispatchEvent("paint", {day:day, hour:hour, newColor:color});
		}
	}
	
	this.clear = function() {
		for (var i = 0; i < this.width; i ++) {
			for (var j = 0; j < this.height; j++) {
				if(this.days[i][j] != null) {
					delete this.days[i][j];
					this.dispatchEvent("paint", {day:i, hour:j, newColor:"blank"});
				}
			}
		}
	}
	
	this.getTimeblocks = function() {
		var timeblocks = [];
		var inTimeblock = false;
		var timeblockStart;
		for (var i = 0; i < this.width; i ++) {
			for (var j = 0; j < this.height; j++) {
				if (this.getColor(i, j) == "blank") {
					if (inTimeblock) {
						timeblocks.push({start:timeblockStart, end:{day:i,hour:j}});
						inTimeblock = false;
					}
				} else {
					if (!inTimeblock) {
						inTimeblock = true;
						timeblockStart = {day:i,hour:j};
					}
				}	
			}
		}
		return timeblocks;
	}
	
	this.getPostableTimeblocks = function(earliestDateOnSchedule) {
		var time = [];
		var timeblocks = this.getTimeblocks();
		for (var i = 0; i < timeblocks.length; i++) {
			var block = timeblocks[i];
			var startDate = new Date();
			startDate.setDate(earliestDateOnSchedule.getDate() + block.start.day);
			startDate.setHours(block.start.hour);
			
			var endDate = new Date();
			endDate.setDate(earliestDateOnSchedule.getDate() + block.end.day);
			endDate.setHours(block.end.hour);
			
			time.push(startDate.getFullYear() + " " + startDate.getMonth() + " " + 
					  startDate.getDate() + " " + startDate.getHours() + " " +
					  endDate.getFullYear() + " " + endDate.getMonth() + " " +
					  endDate.getDate() + " " + endDate.getHours());
		}
		return time;
	}
	
	this.getColor = function(day, hour) {
		if (this.days[day][hour] == null) {
			return "blank";
		}
		return this.days[day][hour];
	}

	this.allHandlers = new Array();
	
	/**
	 * Dispatch a new event to all the event listeners of a given event type
	 */
	this.dispatchEvent = function(type, details){
		var newEvent = {type:type, details:details};

		if (this.allHandlers[type]){
			for (var i in this.allHandlers[type]){
				this.allHandlers[type][i](newEvent);
			}
		}
	}

	/**
	 * Add a new event listener for a given event type
	 * the parameter 'handler' has to be a function with one parameter which is an event object
	 */
	this.addEventListener = function(eventType, handler){
		if (!this.allHandlers[eventType])
			this.allHandlers[eventType] = [];
		this.allHandlers[eventType].push(handler);
	}
}