var time = 0;
var last = 0;
var size = 600

var background = new Path();
background.add(new Point(0,0));
background.add(new Point(size,0));
background.add(new Point(size,size));
background.add(new Point(0,size));
background.closed=true
background.fillColor='#B21212'

var text = new PointText({
    point: size/2,
    justification: 'center',
    fontSize: 30,
    fillColor: 'white'
});

var center = new Point(300,300);
var myPath = new Path();

hoursCircles = createCircles(center, 200, 4, 20);
minutesCircles = createCircles(center, 100, 6, 10);
secondsCircles = createCircles(center, 50, 6, 5);

function createCircles(center, radius, slices, size){
    var circles = [];

    var step = (2*Math.PI)/slices;
    for(var i=0; i<slices; ++i){
        var x = Math.cos(step*i)*radius;
        var y = Math.sin(step*i)*radius;
        x+=center.x;
        y+=center.y;

        circles.push(new Path.Circle(new Point(x,y),size));
        circles[i].fillColor='#FF0001';
    }
    return circles;
}

function secondPath(center, radius, time){
    myPath.clear()
        myPath.strokeColor = '#1486CC';
    myPath.strokeWidth = 10
        var angle = (2*Math.PI)/60;

    for(var i=0; i<time+1; ++i){
        var x = Math.cos(angle*i)*radius;
        var y = Math.sin(angle*i)*radius;
        x+=center.x;
        y+=center.y;
        myPath.add(new Point(x, y));
    }
    return myPath;
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

    secondPath(center, 50, seconds)
        text.content = seconds

        for(var i=0; i<bHours.length; ++i){
            if(bHours[i]==0)
                hoursCircles[i].fillColor='#FF0001'
            else
                hoursCircles[i].fillColor='#0971B2'
        }
    for(var i=0; i<6; ++i){
        if(bMinutes[i]==undefined || bMinutes[i]==0)
            minutesCircles[i].fillColor='#FF0001'
        else
            minutesCircles[i].fillColor='#FFFC19'
    }
    /*for(var i=0; i<6; ++i){
      if(bSeconds[i]==undefined || bSeconds[i]==0)
      secondsCircles[i].fillColor='grey'
      else
      secondsCircles[i].fillColor='red'
      }*/
}
