var size = 900;
var TAU = Math.PI*2;

var arena = Path.Rectangle(new Point(0,0), new Size(size,size));
arena.fillColor = 'black'

var apples = [];

var snake = {
    speed : 1,
    head : new Point(50,50),
    headSprite : new Path.Circle(new Point(50,50), 5),
    angle : 0,
    length : 10,
    isAlive : true,
    body : new Path(),
    keys : [false,false,false], //left,up,right
    init : function(){
        this.body.strokeColor='yellow';
        this.body.strokeWidth=10;
        this.headSprite.fillColor='yellow';
        this.headSprite.strokeColor='yellow';
    },
    eat : function(){
        this.length+=1;  
    },
    forward : function(){
        this.head+=new Point(Math.cos(this.angle/(TAU))*this.speed,
            Math.sin(this.angle/(TAU))*this.speed);
        this.body.add(this.head);
        if(this.body.segments.length>this.length)
            this.body.removeSegment(0);
        this.headSprite.position=this.head;
    },
    left : function(){
        this.angle-=1;
        this.angle%=360;
    },
    right : function(){
        this.angle+=1; 
        this.angle%=360;
    }
}

snake.init();
function popApple(){
    var apple = new Path.Circle(Point.random()*size,5);
    apple.fillColor='red';
    apples.push(apple);
}

function onKeyDown(event) {
    switch(event.key){
        case 'left':
            snake.keys[0]=true;
            break;
        case 'right':
            snake.keys[2]=true;
            break;
        case 'up':
            snake.keys[1]=true;
            break;
        case 'k':
            popApple();
            break;
    }
}

function onKeyUp(event){
    switch(event.key){
        case 'left':
            snake.keys[0]=false;
            break;
        case 'right':
            snake.keys[2]=false;
            break;
        case 'up':
            snake.keys[1]=false;
            break;
    }
}

var last=0;

function checkCollisions(){
    checkWalls();
    checkApples();
    checkSnakes();
}

function checkSnakes(){
    if(snake.headSprite.getIntersections(snake.body).length>1){
        snake.speed=0;
        snake.isAlive=false;
    }
}

function checkApples(){
    for(var i=0; i<apples.length; ++i){
        if(snake.headSprite.getIntersections(apples[i]).length!=0){
            snake.length+=60;
            snake.eat();
            apples[i].clear();
            apples.splice(i,1);
        }    
    }
}

function checkWalls(){
    if(snake.head.x>=size 
        || snake.head.x<=0 
        || snake.head.y>=size
        || snake.head.y<=0){
        snake.speed=0;
        snake.isAlive=false;
    }
}

function onFrame(event) {
    last+=event.delta;
    if(last<0.01)
        return
    last=0;
    
    if(apples.length===0)
        popApple();
    
    checkCollisions();
    if(snake.isAlive){
        if(snake.keys[0]==true)
            snake.left();
        if(snake.keys[2]==true)
            snake.right();
        if(snake.keys[1]==true)
            snake.speed=1.5;
        else
            snake.speed=1;
    }
    snake.forward()
}