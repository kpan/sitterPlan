var ScheduleTable = function(height, width) {
	this.height = height;
	this.width = width;
	this.days = new Array(this.width);
    // make an empty checkerboard
    for (var i=0; i<=this.width; i++){
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