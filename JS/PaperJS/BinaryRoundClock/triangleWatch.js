var time = 0;
var last = 0;
var size = 1200;

//direction
var VERTICAL = true;
var HORIZONTAL = false;
//sens
var STANDARD = true;
var REVERT = false;

var triBase = 100;
var offset = triBase/10;

var background = new Path();
background.add(new Point(0,0));
background.add(new Point(size,0));
background.add(new Point(size,size));
background.add(new Point(0,size));
background.closed=true;
background.fillColor='#B21212';

var center = new Point(300,300);
var myPath = new Path();

var digits = [];
digits[0] = [];
digits[1] = [];
digits[2] = [];
digits[3] = [];
var numbers = [];
numbers.push(zero);
numbers.push(one);
numbers.push(two);
numbers.push(three);
numbers.push(four);
numbers.push(five);
numbers.push(six);
numbers.push(seven);
numbers.push(eight);
numbers.push(nine);

function zero(tri){
    var digit = [];
    tri.rotate(90);
    tri.position += new Point(triBase/4,-triBase/4);
    digit=digit.concat(line(tri, 4, HORIZONTAL, STANDARD));
    
    //right
    var topRightCorner = digit[digit.length-1].clone();
    topRightCorner.rotate(90);
    topRightCorner.position += new Point(triBase/4, triBase/4+offset);
    digit.push(topRightCorner);
    digit=digit.concat(line(topRightCorner,5,VERTICAL,STANDARD));
    
    //center
    var centerRightCorner = digit[digit.length-1].clone();
    centerRightCorner.rotate(90);
    centerRightCorner.position += new Point(-triBase/4, triBase/4+offset);
    digit.push(centerRightCorner);
    digit=digit.concat(line(centerRightCorner,4,HORIZONTAL,REVERT));
    
    //left
    var botLeftCorner = digit[digit.length-1].clone();
    botLeftCorner.rotate(90);
    botLeftCorner.position += new Point(-triBase/4, -triBase/4-offset);
    digit.push(botLeftCorner);
    digit=digit.concat(line(botLeftCorner,5,VERTICAL,REVERT));
    return digit;
}

function one(tri){
    var digit = [];
    tri.position += new Point(0, offset);
    digit=digit.concat(line(tri, 5, VERTICAL, STANDARD));
    return digit;
}

function two(tri){
    var digit = [];
    //top
    tri.rotate(90);
    tri.position += new Point(triBase/4,-triBase/4);
    digit=digit.concat(line(tri, 4, HORIZONTAL,STANDARD));
    
    //right
    var topRightCorner = digit[digit.length-1].clone();
    topRightCorner.rotate(90);
    topRightCorner.position += new Point(triBase/4, triBase/4);
    digit.push(topRightCorner);
    digit=digit.concat(line(topRightCorner,2,VERTICAL,STANDARD));
    
    //center
    var centerRightCorner = digit[digit.length-1].clone();
    centerRightCorner.rotate(90);
    centerRightCorner.position += new Point(-triBase/4, triBase/4);
    digit.push(centerRightCorner);
    digit=digit.concat(line(centerRightCorner,4,HORIZONTAL,REVERT));
    
    //left
    var centerLeftCorner = digit[digit.length-1].clone();
    centerLeftCorner.rotate(270);
    centerLeftCorner.position += new Point(-triBase/4, triBase/4);
    digit.push(centerLeftCorner);
    digit=digit.concat(line(centerLeftCorner,2,VERTICAL,STANDARD));
    
    //bottom
    var botLeftCorner = digit[digit.length-1].clone();
    botLeftCorner.rotate(90);
    botLeftCorner.position += new Point(triBase/4, triBase/4);
    digit.push(botLeftCorner);
    digit=digit.concat(line(botLeftCorner,4,HORIZONTAL,STANDARD));
    botLeftCorner.segments[0].point.x+=triBase/2;
    return digit;
}

function three(tri){
    var digit = [];
    //top
    tri.rotate(90);
    tri.position += new Point(triBase/4,-triBase/4);
    digit=digit.concat(line(tri, 4, HORIZONTAL,STANDARD));
    
    //right
    var topRightCorner = digit[digit.length-1].clone();
    topRightCorner.rotate(90);
    topRightCorner.position += new Point(triBase/4, triBase/4);
    digit.push(topRightCorner);
    digit=digit.concat(line(topRightCorner,2,VERTICAL,STANDARD));
    
    //center
    var centerRightCorner = digit[digit.length-1].clone();
    centerRightCorner.rotate(90);
    centerRightCorner.position += new Point(-triBase/4, triBase/4);
    digit.push(centerRightCorner);
    digit=digit.concat(line(centerRightCorner,4,HORIZONTAL,REVERT));
    
    //right
    var midRightCorner = digit[digit.length-5].clone();
    midRightCorner.rotate(90);
    midRightCorner.position += new Point(triBase/4, triBase/4);
    digit.push(midRightCorner);
    digit=digit.concat(line(midRightCorner,2,VERTICAL,STANDARD));
    
    //bottom
    var botRightCorner = digit[digit.length-1].clone();
    botRightCorner.rotate(90);
    botRightCorner.position += new Point(-triBase/4, triBase/4);
    digit.push(botRightCorner);
    digit=digit.concat(line(botRightCorner,4,HORIZONTAL,REVERT));
    
    return digit;
}

function four(tri){
    var digit = [];
    tri.position += new Point(0, offset);
    digit=digit.concat(line(tri, 2, VERTICAL, STANDARD));
    
    //center
    var centerLeftCorner = digit[digit.length-1].clone();
    centerLeftCorner.rotate(90);
    centerLeftCorner.position += new Point(-triBase/4, triBase/4);
    digit.push(centerLeftCorner);
    digit=digit.concat(line(centerLeftCorner,3,HORIZONTAL,STANDARD));
    
    //top-right
    var centerRightCorner = digit[digit.length-1].clone();
    centerRightCorner.rotate(-90);
    centerRightCorner.position += new Point(triBase/4, -triBase/4);
    digit.push(centerRightCorner);
    digit=digit.concat(line(centerRightCorner, 2, VERTICAL, REVERT));
    //bot-right
    digit=digit.concat(line(centerRightCorner, 3, VERTICAL, STANDARD));
    digit[digit.length-3].segments[2].point.y-=offset;
    digit[digit.length-3].segments[2].point.x+=0;
    return digit;
}

function five(tri){
    var digit = [];
    //top
    tri.rotate(90);
    tri.position += new Point(triBase/4,-triBase/4);
    digit=digit.concat(line(tri, 3, HORIZONTAL,STANDARD));
    
    //left
    var topLeftCorner = tri.clone();
    topLeftCorner.rotate(-90);
    topLeftCorner.position += new Point(-triBase/4, triBase/4+offset);
    digit.push(topLeftCorner);
    digit=digit.concat(line(topLeftCorner,2,VERTICAL,STANDARD));
    
    //center
    var centerLeftCorner = digit[digit.length-1].clone();
    centerLeftCorner.rotate(90);
    centerLeftCorner.position += new Point(-triBase/4, triBase/4);
    digit.push(centerLeftCorner);
    digit=digit.concat(line(centerLeftCorner,4,HORIZONTAL,STANDARD));
    
    //right
    var centerRightCorner = digit[digit.length-1].clone();
    centerRightCorner.rotate(90);
    centerRightCorner.position += new Point(triBase/4, triBase/4+offset);
    digit.push(centerRightCorner);
    digit=digit.concat(line(centerRightCorner,2,VERTICAL,STANDARD));
    
    //bottom
    var botLeftCorner = digit[digit.length-1].clone();
    botLeftCorner.rotate(90);
    botLeftCorner.position += new Point(-triBase/4, triBase/4+offset);
    digit.push(botLeftCorner);
    digit=digit.concat(line(botLeftCorner,3,HORIZONTAL,REVERT));
    return digit;
}

function six(tri){
    var digit = [];
    //top
    tri.rotate(90);
    tri.position += new Point(triBase/4,-triBase/4);
    digit=digit.concat(line(tri, 3, HORIZONTAL,STANDARD));
    
    //left
    var topLeftCorner = tri.clone();
    topLeftCorner.rotate(-90);
    topLeftCorner.position += new Point(-triBase/4, triBase/4+offset);
    digit.push(topLeftCorner);
    digit=digit.concat(line(topLeftCorner,2,VERTICAL,STANDARD));
    
    //center
    var centerLeftCorner = digit[digit.length-1].clone();
    centerLeftCorner.rotate(90);
    centerLeftCorner.position += new Point(-triBase/4, triBase/4);
    digit.push(centerLeftCorner);
    digit=digit.concat(line(centerLeftCorner,4,HORIZONTAL,STANDARD));
    
    //right
    var centerRightCorner = digit[digit.length-1].clone();
    centerRightCorner.rotate(90);
    centerRightCorner.position += new Point(triBase/4, triBase/4+offset);
    digit.push(centerRightCorner);
    digit=digit.concat(line(centerRightCorner,2,VERTICAL,STANDARD));
    
    //bottom
    var botLeftCorner = digit[digit.length-1].clone();
    botLeftCorner.rotate(90);
    botLeftCorner.position += new Point(-triBase/4, triBase/4+offset);
    digit.push(botLeftCorner);
    digit=digit.concat(line(botLeftCorner,3,HORIZONTAL,REVERT));
    
    //bot-left
    var botLeftCorner = digit[digit.length-1].clone();
    botLeftCorner.rotate(-90);
    botLeftCorner.position += new Point(-triBase/4-offset, -triBase/4);
    digit.push(botLeftCorner);
    digit=digit.concat(line(botLeftCorner,2,VERTICAL,REVERT));
    return digit;
}

function seven(tri){
    var digit = [];
    //top
    tri.rotate(90);
    tri.position += new Point(triBase/4,-triBase/4);
    digit=digit.concat(line(tri, 4, HORIZONTAL,STANDARD));
    
    //right
    var topRightCorner = digit[digit.length-1].clone();
    topRightCorner.rotate(90);
    topRightCorner.position += new Point(triBase/4, triBase/4+offset);
    digit.push(topRightCorner);
    digit=digit.concat(line(topRightCorner,5,VERTICAL,STANDARD));
    
    return digit;
}

function eight(tri){
    var digit = [];
    //top
    tri.rotate(90);
    tri.position += new Point(triBase/4,-triBase/4);
    digit=digit.concat(line(tri, 3, HORIZONTAL,STANDARD));
    
    //left
    var topLeftCorner = tri.clone();
    topLeftCorner.rotate(-90);
    topLeftCorner.position += new Point(-triBase/4, triBase/4+offset);
    digit.push(topLeftCorner);
    digit=digit.concat(line(topLeftCorner,2,VERTICAL,STANDARD));
    
    var centerLeftCorner = digit[digit.length-1].clone();
    //top-right
    var topRightCorner = digit[2].clone();
    topRightCorner.rotate(90);
    topRightCorner.position += new Point(triBase/4+offset, triBase/4+offset);
    digit.push(topRightCorner);
    digit=digit.concat(line(topRightCorner,2,VERTICAL,STANDARD));
    
    //center
    centerLeftCorner.rotate(90);
    centerLeftCorner.position += new Point(-triBase/4, triBase/4);
    digit.push(centerLeftCorner);
    digit=digit.concat(line(centerLeftCorner,4,HORIZONTAL,STANDARD));
    
    //right
    var centerRightCorner = digit[digit.length-1].clone();
    centerRightCorner.rotate(90);
    centerRightCorner.position += new Point(triBase/4, triBase/4+offset);
    digit.push(centerRightCorner);
    digit=digit.concat(line(centerRightCorner,2,VERTICAL,STANDARD));
    
    //bottom
    var botLeftCorner = digit[digit.length-1].clone();
    botLeftCorner.rotate(90);
    botLeftCorner.position += new Point(-triBase/4, triBase/4+offset);
    digit.push(botLeftCorner);
    digit=digit.concat(line(botLeftCorner,3,HORIZONTAL,REVERT));
    
    //bot-left
    var botLeftCorner = digit[digit.length-1].clone();
    botLeftCorner.rotate(-90);
    botLeftCorner.position += new Point(-triBase/4-offset, -triBase/4);
    digit.push(botLeftCorner);
    digit=digit.concat(line(botLeftCorner,2,VERTICAL,REVERT));
    return digit;
}

function nine(tri){
    var digit = [];
    //top
    tri.rotate(90);
    tri.position += new Point(triBase/4,-triBase/4);
    digit=digit.concat(line(tri, 3, HORIZONTAL,STANDARD));
    
    //left
    var topLeftCorner = tri.clone();
    topLeftCorner.rotate(-90);
    topLeftCorner.position += new Point(-triBase/4, triBase/4+offset);
    digit.push(topLeftCorner);
    digit=digit.concat(line(topLeftCorner,2,VERTICAL,STANDARD));
    
    var centerLeftCorner = digit[digit.length-1].clone();
    //top-right
    var topRightCorner = digit[2].clone();
    topRightCorner.rotate(90);
    topRightCorner.position += new Point(triBase/4+offset, triBase/4+offset);
    digit.push(topRightCorner);
    digit=digit.concat(line(topRightCorner,2,VERTICAL,STANDARD));
    
    //center
    centerLeftCorner.rotate(90);
    centerLeftCorner.position += new Point(-triBase/4, triBase/4);
    digit.push(centerLeftCorner);
    digit=digit.concat(line(centerLeftCorner,4,HORIZONTAL,STANDARD));
    
    //right
    var centerRightCorner = digit[digit.length-1].clone();
    centerRightCorner.rotate(90);
    centerRightCorner.position += new Point(triBase/4, triBase/4+offset);
    digit.push(centerRightCorner);
    digit=digit.concat(line(centerRightCorner,2,VERTICAL,STANDARD));
    
    //bottom
    var botLeftCorner = digit[digit.length-1].clone();
    botLeftCorner.rotate(90);
    botLeftCorner.position += new Point(-triBase/4, triBase/4+offset);
    digit.push(botLeftCorner);
    digit=digit.concat(line(botLeftCorner,3,HORIZONTAL,REVERT));
    return digit;
}

function line(copy, times, direction, sens){
    var digit = [];
    for(var i=0; i<times; ++i){
        var copy = copy.clone();
        copy.rotate(180);
        if(sens==STANDARD){
            copy.position += new Point(direction?0:(triBase/2)+offset,
            direction?(triBase/2)+offset:0);
        }else{
            copy.position -= new Point(direction?0:(triBase/2)+offset,
            direction?(triBase/2)+offset:0);
        }
        digit.push(copy);
    }
    return digit;
}

function triangle(offset){
    var tri = new Path();
    tri.add(new Point(0+offset,0));
    tri.add(new Point(0+offset,triBase));
    tri.add(new Point(triBase/2+offset, triBase/2));
    tri.closed=true
    tri.fillColor='black'
    return tri;
}

function clearDigits(){
    for(var i=0; i<digits.length; ++i){
        for(var j=0; j<digits[i].length;++j){
            digits[i][j].clear();
        }
    }
}

function onFrame(event) {
    last += event.delta;
    if(last>=1){
        time+=1;
        last=0;
    }else{
        return   
    }
    //86400s in a day
    if(time>86400)
        time=0;
        
    hours = parseInt(time/3600);
    minutes = parseInt((time%3600)/60);
    seconds = time%60;
    
    clearDigits();
    
    var tri = triangle(0);
    digits[0].push(tri);
    digits[0]=digits[0].concat(numbers[parseInt(seconds/10)](tri));
    
    var tri = triangle(400);
    digits[0].push(tri);
    digits[0]=digits[0].concat(numbers[seconds%10](tri));
    
    var size = 0;
    for(var i=0; i<digits.length; ++i){
        for(var j=0; j<digits[i].length;++j){
            size+=digits[i].length;
        }
    }
    for(var i=0; i<digits.length; ++i){
        for(var j=0; j<digits[i].length;++j){
            if(seconds!=0){
                digits[i][j].fillColor='yellow';
                seconds--;
            }else{
                digits[i][j].fillColor='black';
            }
        }
    }
    
    /*bHours = hours.toString(2);
    bMinutes = minutes.toString(2);
    bSeconds = seconds.toString(2);
    bHours = bHours.split('').reverse().join('');
    bMinutes = bMinutes.split('').reverse().join('');
    bSeconds = bSeconds.split('').reverse().join('');*/
}