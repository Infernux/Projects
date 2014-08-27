var time = 0;
var last = 0;

hoursCircles = createCircles(new Point(300,300), 200, 4, 20);
minutesCircles = createCircles(new Point(300,300), 100, 6, 10);
secondsCircles = createCircles(new Point(300,300), 50, 6, 5);

function createCircles(center, radius, slices, size){
    var circles = [];

    var step = (2*Math.PI)/slices;
    for(var i=0; i<slices; ++i){
        var x = Math.cos(step*i)*radius;
        var y = Math.sin(step*i)*radius;
        x+=center.x;
        y+=center.y;

        circles.push(new Path.Circle(new Point(x,y),size));
        circles[i].fillColor='black';
    }
    return circles;
}

function onFrame(event) {
    last += event.delta;
    if(last>=1){
        time+=1;
        last=0;
    }
    //86400s in a day
    if(time>86400)
        time=0;

    hours = parseInt(time/3600);
    minutes = parseInt((time%3600)/60);
    seconds = time%60;

    bHours = hours.toString(2);
    bMinutes = minutes.toString(2);
    bSeconds = seconds.toString(2);
    bHours = bHours.split('').reverse().join('');
    bMinutes = bMinutes.split('').reverse().join('');
    bSeconds = bSeconds.split('').reverse().join('');

    for(var i=0; i<bHours.length; ++i){
        if(bHours[i]==0)
            hoursCircles[i].fillColor='black'
        else
            hoursCircles[i].fillColor='red'
    }
    for(var i=0; i<6; ++i){
        if(bMinutes[i]==undefined || bMinutes[i]==0)
            minutesCircles[i].fillColor='black'
        else
            minutesCircles[i].fillColor='red'
    }
    for(var i=0; i<6; ++i){
        if(bSeconds[i]==undefined || bSeconds[i]==0)
            secondsCircles[i].fillColor='black'
        else
            secondsCircles[i].fillColor='red'
    }
    console.log(hours,'h ',minutes,'m ',seconds,'s')
}
