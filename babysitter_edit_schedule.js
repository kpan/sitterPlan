	//the times on the schedule to display (controlled by the slider)
	var earliestTimeOnSchedule = 13;
	var latestTimeOnSchedule = 24;
	//color to paint in, currently always green
	var currentColor = "green";
	//whether the mouse button is down
	var painting = false;
	//the first date to display (currently always today)
	var earliestDateOnSchedule = new Date();

	//representation of which things are colored
	var babysitterScheduleTable = new ScheduleTable(24, 7);
	
	//update the displayed table with new information if stuff gets painted
	babysitterScheduleTable.addEventListener('paint',function (e) {
		if (e.details.newColor == "green") {
			$( "#" + e.details.day + "_" + e.details.hour + "_square").attr('class', 'greenScheduleTableSquare');
		} else if (e.details.newColor == "blank") {
			$( "#" + e.details.day + "_" + e.details.hour + "_square").attr('class', 'blankScheduleTableSquare');
		}
    },true);
	
	//initialization things
	$(function() {
		// add all the rows for the various hours of days to the table you can paint
		for (var i = earliestTimeOnSchedule; i < latestTimeOnSchedule; i ++){
			$("#babysitterScheduleTable > tbody > tr:last").after(genRow(i));
		}
		
		// make the labels for the columns
		for (var i = 0; i < 7; i++) {
			var tempDate = new Date();
			tempDate.setDate(earliestDateOnSchedule.getDate() + i);
			var dateString = tempDate.toDateString();
			dateString = dateString.substring(0, dateString.length - 4);
			$("#day" + i).text(dateString);
		}
		
		updateEditingSchedule();
		
		// initialize the slider for which times are showing
		makeSlider();
  	});
	
	// track whether the mouse button is down
	document.onmousedown = function() {
		painting = true;
	}
	
	document.onmouseup = function() {
		painting = false;
	}

	//all schedule stuff is same-each-week.
	function updateEditingSchedule() {
		$.get("schedule/jimmy/", function(data) {
			var lines = data.split("\n");
			for (line in lines) {
				var fields = lines[line].split(" ");
				if (fields.length == 4) { //validate it's a real line
					paintRange(parseInt(fields[0]), parseInt(fields[1]), parseInt(fields[2]), parseInt(fields[3]));
				}
			}
		});
	}
	
	function paintRange(startDay, startHour, endDay, endHour) {
		if (startDay != endDay) {
			paintRange(startDay, startHour, startDay, 24);
			paintRange((startDay + 1)%7, 0, endDay, endHour);
		} else {
			if (startHour < endHour){
				var relDay = (startDay - earliestDateOnSchedule.getDay());
				if (relDay < 0) {
					relDay = relDay + 7;
				}
				babysitterScheduleTable.paint(relDay, startHour, "green");
				paintRange(startDay, startHour + 1, endDay, endHour);
			}
		}
	}
	
	//initialize the slider for which times are showing.
	function makeSlider() {
		$( "#timerange-slider" ).slider({range: true, min: 0, max:24,
									 orientation:"vertical",
									 values:[ 24 - latestTimeOnSchedule,
									 		  24 - earliestTimeOnSchedule ],
									 slide: function( event, ui ) {
										 		updateTimerange( 24 - ui.values[1],
												           24 - ui.values[0]);
									 }}).height("300px");
		$( "#timerange-slider > a:first").text(asShort12HourTime(latestTimeOnSchedule)).addClass("sliderLabel");
		$( "#timerange-slider > a:last").text(asShort12HourTime(earliestTimeOnSchedule)).addClass("sliderLabel");
	}
	
	
	// on mouseover to a table cell, paint it if the mouse button's down
	function paintIfClicking(event, day, time) {
		if (painting) {
			babysitterScheduleTable.paint(day, time, currentColor);
		}
	}

	// make a row for the table: makes a bunch of table cells with appropriate event handlers
	function genRow(time) {
		var row = "<tr class='scheduleTableRow' id='" + as12HourTime(time) + "row" + 
				  "'>\n<td class='scheduleRowLabel'>";
		row += as12HourTime(time) + "</td>\n";
		for (var day = 0; day < babysitterScheduleTable.width; day ++) {
			row += "<td class='";
			row += babysitterScheduleTable.getColor(day,time) + "ScheduleTableSquare";
			row += "' id='" + day + "_" + time + "_square' ";
			row += "onmousedown='babysitterScheduleTable.paint(" + day + "," + time + ", currentColor)' ";
			row += "onmouseover='paintIfClicking(event," + day + "," + time + ")'/>\n";
		}
		row += "</tr>\n"
		return row;
	}
	
	// scale the table appropriately when the slider moves	
	function updateTimerange(startTime, endTime){
		$( "#startTime").text(as12HourTime(startTime));
		$( "#endTime").text(as12HourTime(endTime));
		
		$( "#timerange-slider > a:first").text(asShort12HourTime(endTime));
		$( "#timerange-slider > a:last").text(asShort12HourTime(startTime));
		
		for (var i = earliestTimeOnSchedule; i < startTime; i++) {
			$("#" + as12HourTime(i) + "row").remove();
		}
		
		for (var i = startTime; i < endTime; i ++){
			if (i < earliestTimeOnSchedule || i >= latestTimeOnSchedule) {
				$("#babysitterScheduleTable > tbody > tr").eq(i - startTime).after(genRow(i));
			}
		}
		for (var i = endTime; i < latestTimeOnSchedule; i++) {
			$("#" + as12HourTime(i) + "row").remove();
		}
		earliestTimeOnSchedule = startTime;
		latestTimeOnSchedule = endTime;
	}
	
	// convert a number to a nice time like "5am"
	function as12HourTime(number) {
		if (number == 0 || number == 24) {
			return "midnight";
		}
		if (number < 12) {
			return number + "am";
		}
		if (number == 12) {
			return "noon";
		} else {
			return (number - 12) + "pm";
		}
	}	

	// convert a number to a short time like "5"
	function asShort12HourTime(number) {
		if (number == 0) {
			return 12;
		}
		if (number <= 12) {
			return number;
		}
		return number - 12;
	}
	
	// close the dialog, submit to the server
	function submitSchedule() {
		$.post("schedule/jimmy/", {times:babysitterScheduleTable.getPostableTimeblocks(earliestDateOnSchedule)}, 
			   function(data){updateCalendar();});
		$("#hidingDiv").append($("#editSchedulePopup").remove());
		$("#editSchedulePopup").dialog('close');
	}
	
	// show the schedule editing popup
	function showEditSchedule(){
		$("#hidingDiv").append($("#editSchedulePageOne").detach());
		$("#hidingDiv").append($("#editSchedulePageTwo").detach());
      	dialog = $("#editSchedulePopup").dialog({title:"Edit Your Schedule",
									 modal:true, 
									 draggable:false,
									 width:800, 
									 height:600}).addClass("bodyFont").append($("#editSchedulePageOne"));
		makeSlider();
  	}
	
	// clears the schedule in the dialog.
	function clearSchedule() {
		var timeblocks = babysitterScheduleTable.getTimeblocks();
		for (var i = 0; i < timeblocks.length; i++) {
			var block = timeblocks[i];
			for(var day = block.start.day; day <= block.end.day; day++) {
				for(var time = earliestTimeOnSchedule; time <= latestTimeOnSchedule; time++) {
					babysitterScheduleTable.paint(day, time, "blank");
				}
			}
		}
	}
	
	// show the contacts managing popup
	function showManageContacts(){
      	$("#manageContactsPopup").dialog({title:"Manage Contacts",
									 modal:true, 
									 draggable:false, 
									 width:800, 
									 height:600}).addClass("bodyFont");
  	}
	
	function showApplyJobPopup(jobId){
		$.get("jobApplicationPopup/jimmy/" + jobId + "/", function(data){$("#applyJobPopup").html(data);$("#applyJobPopup").dialog({title:"Apply for this job?"});});
	}
	
	function showUnApplyJobPopup(jobId){
		$.get("jobUnApplicationPopup/jimmy/" + jobId + "/", function(data){$("#applyJobPopup").html(data);$("#applyJobPopup").dialog({title:"Withdraw your application?"});});
	}

    function clearSchedule(){
    	babysitterScheduleTable.clearAll();
    }