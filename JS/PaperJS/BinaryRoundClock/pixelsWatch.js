var time = 0;
var last = 0;
var size = 1200;
var subPixelSize = 10;
var subPixelSpacing = 1;
var subPixel = subPixelSize+subPixelSpacing;
var pixelSpacing = 3*subPixelSize+3*subPixelSpacing;

//direction
var VERTICAL = true;
var HORIZONTAL = false;
//sens
var STANDARD = true;
var REVERSE = false;

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

function zero(offset){
    var digit = [];
    digit=digit.concat(line(new Point(0,0)+offset,5,VERTICAL,STANDARD));
    digit=digit.concat(line(new Point(pixelSpacing,0)+offset,1,HORIZONTAL,STANDARD));
    digit=digit.concat(line(new Point(pixelSpacing*2,0)+offset,5,VERTICAL,STANDARD));
    digit=digit.concat(line(new Point(pixelSpacing,pixelSpacing*4)+offset,1,HORIZONTAL,STANDARD));
    //digit=digit.concat(basePixel(new Point(0,0)));
    return digit;
}

function one(offset){
    var digit = [];
    digit=digit.concat(line(new Point(0,0)+offset,5,VERTICAL,STANDARD));
    return digit;
}

function two(offset){
    var digit = [];
    digit=digit.concat(line(new Point(0,0)+offset,3,HORIZONTAL,STANDARD));
    digit=digit.concat(line(new Point(pixelSpacing*2,pixelSpacing*1)+offset,2,VERTICAL,STANDARD));
    digit=digit.concat(line(new Point(pixelSpacing,pixelSpacing*2)+offset,2,HORIZONTAL,REVERSE));
    digit=digit.concat(line(new Point(0,pixelSpacing*3)+offset,2,VERTICAL,STANDARD));
    digit=digit.concat(line(new Point(pixelSpacing,pixelSpacing*4)+offset,2,HORIZONTAL,STANDARD));
    return digit;
}

function three(offset){
    var digit = [];
    digit=digit.concat(line(new Point(0,0)+offset,3,HORIZONTAL,STANDARD));
    digit=digit.concat(line(new Point(pixelSpacing*2,pixelSpacing*1)+offset,2,VERTICAL,STANDARD));
    digit=digit.concat(line(new Point(pixelSpacing,pixelSpacing*2)+offset,2,HORIZONTAL,REVERSE));
    digit=digit.concat(line(new Point(pixelSpacing*2,pixelSpacing*3)+offset,2,VERTICAL,STANDARD));
    digit=digit.concat(line(new Point(pixelSpacing,pixelSpacing*4)+offset,2,HORIZONTAL,REVERSE));
    return digit;
}

function four(offset){
    var digit = [];
    digit=digit.concat(line(new Point(0,0)+offset,2,VERTICAL,STANDARD));
    digit=digit.concat(line(new Point(0,pixelSpacing*2)+offset,2,HORIZONTAL,STANDARD));
    digit=digit.concat(line(new Point(pixelSpacing*2,0)+offset,5,VERTICAL,STANDARD));
    return digit;
}

function five(offset){
    var digit = [];
    digit=digit.concat(line(new Point(pixelSpacing*2,0)+offset,3,HORIZONTAL,REVERSE));
    digit=digit.concat(line(new Point(0,pixelSpacing)+offset,2,VERTICAL,STANDARD));
    digit=digit.concat(line(new Point(0,pixelSpacing*2)+offset,3,HORIZONTAL,STANDARD));
    digit=digit.concat(line(new Point(pixelSpacing*2,pixelSpacing*3)+offset,2,VERTICAL,STANDARD));
    digit=digit.concat(line(new Point(pixelSpacing,pixelSpacing*4)+offset,2,HORIZONTAL,REVERSE));
    return digit;
}

function six(offset){
    var digit = [];
    digit=digit.concat(line(new Point(pixelSpacing*2,0)+offset,3,HORIZONTAL,REVERSE));
    digit=digit.concat(line(new Point(0,pixelSpacing)+offset,4,VERTICAL,STANDARD));
    digit=digit.concat(line(new Point(0,pixelSpacing*4)+offset,3,HORIZONTAL,STANDARD));
    digit=digit.concat(line(new Point(pixelSpacing*2,pixelSpacing*3)+offset,2,VERTICAL,REVERSE));
    digit=digit.concat(line(new Point(pixelSpacing,pixelSpacing*2)+offset,1,HORIZONTAL,REVERSE));
    return digit;
}

function seven(offset){
    var digit = [];
    digit=digit.concat(line(new Point(0,0)+offset,3,HORIZONTAL,STANDARD));
    digit=digit.concat(line(new Point(pixelSpacing*2,pixelSpacing)+offset,4,VERTICAL,STANDARD));
    return digit;
}

function eight(offset){
    var digit = [];
    digit=digit.concat(line(new Point(0,0)+offset,5,VERTICAL,STANDARD));
    digit=digit.concat(line(new Point(pixelSpacing*2,0)+offset,5,VERTICAL,STANDARD));
    digit=digit.concat(line(new Point(pixelSpacing,0)+offset,1,HORIZONTAL,STANDARD));
    digit=digit.concat(line(new Point(pixelSpacing,pixelSpacing*2)+offset,1,HORIZONTAL,STANDARD));
    digit=digit.concat(line(new Point(pixelSpacing,pixelSpacing*4)+offset,1,HORIZONTAL,STANDARD));
    return digit;
}

function nine(offset){
    var digit = [];
    digit=digit.concat(line(new Point(pixelSpacing,pixelSpacing*2)+offset,2,HORIZONTAL,REVERSE));
    digit=digit.concat(line(new Point(0,pixelSpacing)+offset,2,VERTICAL,REVERSE));
    digit=digit.concat(line(new Point(pixelSpacing,0)+offset,2,HORIZONTAL,STANDARD));
    digit=digit.concat(line(new Point(pixelSpacing*2,pixelSpacing)+offset,4,VERTICAL,STANDARD));
    digit=digit.concat(line(new Point(pixelSpacing,pixelSpacing*4)+offset,2,HORIZONTAL,REVERSE));
    return digit;
}

function line(offset, times, direction, sens){
    var digit = [];
    for(var i=0; i<times; ++i){
        var pixel = basePixel(offset);
        digit = digit.concat(pixel);
        if(sens==STANDARD){
            offset += new Point(direction==true?0:3*subPixel,
                direction==true?3*subPixel:0);
        }else{
            offset -= new Point(direction?0:3*subPixel,
                direction?3*subPixel:0);
        }
    }
    return digit;
}

function basePixel(offset){
    var res = [];
    var size = new Size(subPixelSize, subPixelSize);
    var offset = offset.clone();
    yOff = offset.y;
    for(var i=0; i<3; ++i){
        for(var j=0; j<3; ++j){
            res.push(new Path.Rectangle(offset, size));
            offset.y += subPixelSize+subPixelSpacing;
        }
        offset.x += subPixelSize+subPixelSpacing;
        offset.y = yOff;
    }
    return res;
}

function clearDigits(){
    for(var i=0; i<digits.length; ++i){
        for(var j=0; j<digits[i].length;++j){
            digits[i][j].clear();
        }
        digits[i]=[];
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
    
    digits[0]=digits[0].concat(numbers[parseInt(minutes/10)](new Point(0,0)));
    
    digits[1]=digits[1].concat(numbers[minutes%10](new Point(150,0)));
    //digits[1]=digits[1].concat(numbers[0](pixel));
    
    var size = 0;
    for(var i=0; i<digits.length; ++i){
        size+=digits[i].length;
    }
    var step = size/60;
    step*=seconds;
    
    for(var i=0; i<digits.length; ++i){
        for(var j=0; j<digits[i].length;++j){
            if(step>=1){
                digits[i][j].fillColor='yellow';
                step--;
            }else if(step>=0){
                digits[i][j].fillColor='yellow';
                step--;
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