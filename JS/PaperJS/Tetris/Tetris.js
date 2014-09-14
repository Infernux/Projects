var DEBUG = false;

var size = 900;
var width = 400;
var height = 800;
var gridSize = width/10;
var offset = 50;
var TAU = Math.PI*2;

var creators = [];

var hauteur = 20, largeur = 10;

var grid = [];
var pieces = [];
var compounds = [];

var activePiece = null;

var keys=[false,false,false,false,false];

var valScore;
var lvl;

//backgrounds
var bg = Path.Rectangle(new Point(0,0), new Size(size,size));
bg.fillColor = 'black'

var fps = new PointText({
	point: new Point(30,30),
	justification: 'center',
	fontSize: 30,
	fillColor: 'white'
});

var score = new PointText({
	point: new Point(width+offset+50,offset+30),
	justification: 'left',
	fontSize: 30,
	fillColor: 'white'
});

var arena = new Path();
arena.add(new Point(offset,offset));
arena.add(new Point(offset,offset+height));
arena.add(new Point(offset+width,offset+height));
arena.add(new Point(offset+width,offset));
arena.strokeColor='white';

creators.push(createLine);
creators.push(createL);
creators.push(createRevertL);
creators.push(createSquare);
creators.push(createS);
creators.push(createRevertS);
creators.push(createT);

init();
spawn();

function onKeyDown(event) {
    switch(event.key){
        case 'left':
            keys[0]=true;
            break;
        case 'right':
            keys[3]=true;
            break;
        case 'up':
            keys[1]=true;
            break;
        case 'down':
            keys[2]=true;
            break;
        case 'control':
            keys[4]=true;
            break;
    }
}

function onKeyUp(event){
    switch(event.key){
        case 'left':
            keys[0]=false;
            break;
        case 'right':
            keys[3]=false;
            break;
        case 'up':
            keys[1]=false;
            break;
        case 'down':
            keys[2]=false;
            break;
        case 'control':
            keys[4]=false;
            break;
    }
}

function createLine(){
    var line = new CompoundPath();
    var base = Path.Rectangle(new Point(0,0), new Size(width/10,width/10));
    
    line.addChild(base);
    var sec = base.clone();
    sec.position.x+=gridSize;
    line.addChild(sec);
    sec = base.clone();
    sec.position.x+=gridSize*2;
    line.addChild(sec);
    sec = base.clone();
    sec.position.x+=gridSize*3
    line.addChild(sec);
    line.strokeColor='black';
    line.width = 4*gridSize;
    line.height = gridSize;
    line.fillColor='red';
    
    line.largeur = 4;
    line.hauteur = 1;
    
    line.mesh=[[-1,0],[0,0],[1,0],[2,0]];
    line.center = new Point(-gridSize/2, gridSize/2);
    line.pivot = new Point(gridSize*2,0);
    
    return line;
}

function createL(){
    var shape = new CompoundPath();
    var base = Path.Rectangle(new Point(0,0), new Size(width/10,width/10));
    shape.addChild(base);
    var sec = base.clone();
    sec.position.x+=gridSize;
    shape.addChild(sec);
    sec = base.clone();
    sec.position.x+=gridSize*2;
    shape.addChild(sec);
    sec = base.clone();
    sec.position.y-=gridSize;
    
    shape.addChild(sec);
    shape.strokeColor='black';
    shape.width = 3*gridSize;
    shape.height = 2*gridSize;
    shape.fillColor='purple';
    
    shape.largeur = 3;
    shape.hauteur = 2;
    
    shape.mesh = [[0,0],[1,0],[2,0],[0,-1]];
    shape.center = new Point(-gridSize/2, gridSize/2);
    shape.pivot = new Point(gridSize,0);
    
    return shape;
}

function createRevertL(){
    var shape = new CompoundPath();
    var base = Path.Rectangle(new Point(0,0), new Size(width/10,width/10));
    shape.addChild(base);
    var sec = base.clone();
    sec.position.x+=gridSize;
    shape.addChild(sec);
    sec = base.clone();
    sec.position.x+=gridSize*2;
    shape.addChild(sec);
    sec = base.clone();
    sec.position.x+=gridSize*2;
    sec.position.y-=gridSize;
    
    shape.addChild(sec);
    shape.strokeColor='black';
    shape.width = 3*gridSize;
    shape.height = 2*gridSize;
    shape.fillColor='green';
    
    shape.largeur = 3;
    shape.hauteur = 2;
    
    shape.mesh = [[-2,0],[-1,0],[0,0],[0,-1]];
    shape.center = new Point(-gridSize/2, gridSize/2);
    shape.pivot = new Point(gridSize*3,0);
    return shape;
}

function createS(){
    var shape = new CompoundPath();
    var base = Path.Rectangle(new Point(0,0), new Size(width/10,width/10));
    shape.addChild(base);
    var sec = base.clone();
    sec.position.x+=gridSize;
    shape.addChild(sec);
    sec = base.clone();
    sec.position.x+=gridSize;
    sec.position.y-=gridSize;
    shape.addChild(sec);
    sec = base.clone();
    sec.position.x+=gridSize*2;
    sec.position.y-=gridSize;
    
    shape.addChild(sec);
    shape.strokeColor='black';
    shape.width = 3*gridSize;
    shape.height = 2*gridSize;
    shape.fillColor='lightblue';
    
    shape.largeur = 3;
    shape.hauteur = 2;
    
    shape.mesh = [[-1,0],[0,0],[0,-1],[1,-1]];
    shape.center = new Point(-gridSize/2, gridSize/2);
    shape.pivot = new Point(gridSize*2,0);
    
    return shape;
}

function createRevertS(){
    var shape = new CompoundPath();
    var base = Path.Rectangle(new Point(-gridSize,-gridSize), new Size(width/10,width/10));
    shape.addChild(base);
    var sec = base.clone();
    sec.position.x+=gridSize;
    shape.addChild(sec);
    sec = base.clone();
    sec.position.x+=gridSize;
    sec.position.y+=gridSize;
    shape.addChild(sec);
    sec = base.clone();
    sec.position.x+=gridSize*2;
    sec.position.y+=gridSize;
    
    shape.addChild(sec);
    shape.strokeColor='black';
    shape.width = 3*gridSize;
    shape.height = 2*gridSize;
    shape.fillColor='green';
    
    shape.largeur = 3;
    shape.hauteur = 2;
    
    shape.mesh = [[-1,-1],[0,-1],[0,0],[1,0]];
    shape.center = new Point(-gridSize/2, gridSize/2);
    shape.pivot = new Point(gridSize,0);
    
    return shape;
}

function createT(){
    var shape = new CompoundPath();
    var base = Path.Rectangle(new Point(-gridSize,0), new Size(width/10,width/10));
    shape.addChild(base);
    var sec = base.clone();
    sec.position.x+=gridSize;
    shape.addChild(sec);
    sec = base.clone();
    sec.position.x+=gridSize;
    sec.position.y-=gridSize;
    shape.addChild(sec);
    sec = base.clone();
    sec.position.x+=gridSize*2;
    
    shape.addChild(sec);
    shape.strokeColor='black';
    shape.width = 3*gridSize;
    shape.height = 2*gridSize;
    shape.fillColor='yellow';
    
    shape.largeur = 3;
    shape.hauteur = 2;
    
    shape.mesh = [[-1,0],[0,0],[0,-1],[1,0]];
    shape.center = new Point(-gridSize/2,gridSize/2);
    shape.pivot = new Point(gridSize,0);
    
    return shape;
}

function createSquare(){
    var shape = new CompoundPath();
    var base = Path.Rectangle(new Point(0,0), new Size(width/10,width/10));
    shape.addChild(base);
    var sec = base.clone();
    sec.position.x+=gridSize;
    shape.addChild(sec);
    sec = base.clone();
    sec.position.y-=gridSize;
    shape.addChild(sec);
    sec = base.clone();
    sec.position.x+=gridSize;
    sec.position.y-=gridSize;
    
    shape.addChild(sec);
    shape.strokeColor='black';
    shape.width = 2*gridSize;
    shape.height = 2*gridSize;
    shape.fillColor='orange';
    
    shape.largeur = 2;
    shape.hauteur = 2;
    
    shape.mesh = [[0,0],[1,0],[0,-1],[1,-1]];
    shape.center = new Point(-gridSize/2, gridSize/2);
    shape.pivot = new Point(gridSize,0);
    return shape;
}

function spawn(){
    var rand = parseInt(Math.random()*creators.length);
    activePiece = creators[rand].call();
        
    activePiece.x = 4;
    activePiece.y = 0;
    activePiece.position = new Point(offset+gridSize*5,
            offset);
}

function removeFilled(){
    var removed = 0;
    for(var j=0; j<hauteur; ++j){
        var res = true;
        for(var i=0; i<largeur; ++i){
            if(grid[i][j]!==1)
                res=false;
        }
        if(res){
            removed++;
            for(var i=0; i<pieces[j].length;++i){
                pieces[j][i].remove();
            }
            for(var j2=j; j2>0; --j2){
                for(var i=0; i<largeur; ++i){
                    grid[i][j2]=grid[i][j2-1];
                }
                pieces[j2]=pieces[j2-1];
                //move all compound paths down by one step
                for(var i=0; i<pieces[j2].length; ++i)
                    pieces[j2][i].position.y+=gridSize;
            }
            pieces[0]=[];
            for(var i=0; i<largeur; ++i){
                grid[i][0]=0;
            }
            
            //clear empty compounds
            for(var i=0; i<compounds.length; ++i){
                if(compounds[i].length==0){
                    compounds[i].remove();
                    compounds.remove(i);
                }
            }
        }
    }
    return removed;
}

function step(){
    var collided = checkCollisions(activePiece,0,1);
    if(!collided){
        for(var i=0; i<activePiece.mesh.length; i++){
            grid[activePiece.x+activePiece.mesh[i][0]]
                [activePiece.y+activePiece.mesh[i][1]]=0;
            grid[activePiece.x+activePiece.mesh[i][0]]
                [activePiece.y+activePiece.mesh[i][1]+1]=-1;    
        }
        activePiece.position.y+=gridSize;
        activePiece.y++;
        return true;
    }
    return false;
}

function checkCollisions(piece, dx, dy){
    var collided = false;
    for(var i=0; i<piece.mesh.length; i++){
        collided=collision(piece.x+piece.mesh[i][0],piece.y+piece.mesh[i][1],dx,dy)
        ||collided;
    }
    return collided;
}

function collision(x,y,dx,dy){
    if(dx!==0 && ((x+dx<0) || (x+dx>=largeur))){
        return -1;
    }
    if(y+dy>=hauteur)
        return true;
    if(grid[x+dx][y+dy]===1)
        return true;
    return false;
}

var last=0, lastTic=0;

function fix(){
    for(var i=0; i<activePiece.mesh.length; i++){
        var y = activePiece.y+activePiece.mesh[i][1];
        grid[activePiece.x+activePiece.mesh[i][0]]
                    [y]=1;
        if(y<0){
            activePiece.clear();
            lose();
            return;
        }
        pieces[y].push(activePiece.children[i]);
    }
    var score = removeFilled();
    increaseScore(score);
    compounds.push(activePiece);
}

function lose(){
    clearAll();
    grid=null;
    init();
}

function clearAll(){
    //clear empty compounds
    for(var i=0; i<pieces.length; ++i){
        for(var j=0; j<pieces[i].length; ++j){
            pieces[i][j].remove();
            pieces[i][j]=null;
        }
        pieces[i]=[];
    }
    for(var i=0; i<compounds.length; ++i){
        for(var c=0; c<compounds[i].length; c++){
            compounds[i].children[c].clear();
            compounds.clear();
            compounds.remove(i);
        }
    }
}

function init(){
    score.content="0"
    valScore=0;
    lvl=1;
    
    grid=[];
    
    for(var i=0; i<largeur; ++i){
        var column = [];
        for(var j=0; j<hauteur; ++j){
            column.push(0);
        }
        grid.push(column);
    }

    for(var j=0; j<hauteur; ++j)
        pieces.push([]);
}

function increaseScore(val){
    switch(val){
        case 1:
            valScore+=40*lvl;
            break;
        case 2:
            valScore+=100*lvl;
            break;
        case 3:
            valScore+=300*lvl;
            break;
        case 4:
            valScore+=1200*lvl;
            break;
    }
    score.content=valScore;
}

//return whether rotation is valid or not
function checkRotation(){
    for(var i=0; i<activePiece.mesh.length; i++){
        var x = activePiece.mesh[i][0];
        var y = activePiece.mesh[i][1];
        
        var res = collision(activePiece.x, activePiece.y, y, -x)
        if(res==-1 || res==true)
            return false;
    }
    return true;
}

//swap(x,y) then y=-y => -90° rotation
function rotate(){
    if(!checkRotation())
        return;
        
    center = new Point(activePiece.position);
    for(var i=0; i<activePiece.mesh.length; i++){
        var x = activePiece.mesh[i][0];
        var y = activePiece.mesh[i][1];
        
        activePiece.mesh[i][0]=y;
        activePiece.mesh[i][1]=-x;
    }
    
    if(DEBUG){
        var base = Path.Rectangle(center, new Size(5,5));
        base.fillColor='red';
        var base = Path.Rectangle(activePiece.position+activePiece.center, new Size(5,5))
        base.fillColor='green';
    }
    
    var x = activePiece.center.x;
    var y = activePiece.center.y;
        
    activePiece.rotate(-90, activePiece.position+activePiece.center);
    activePiece.center.x=y;
    activePiece.center.y=-x;
}

function onFrame(event) {
    last+=event.delta;
    lastTic+=event.delta;
    if(last<0.05)
        return
    last=0;
    fps.content=parseInt(1/event.delta);
    
    if(keys[0]==true)
        if(checkCollisions(activePiece,-1,0)===false){
            activePiece.position.x-=gridSize;
            activePiece.x-=1;
        }
    if(keys[3]==true)
        if(checkCollisions(activePiece,1,0)===false){
            activePiece.position.x+=gridSize;
            activePiece.x+=1;
        }
    if(keys[1]==true)
        rotate(-90);
    if(keys[4]==true)
        rotate(90);
    if(keys[2]==true){
        if(!checkCollisions(activePiece,0,1)){
            activePiece.position.y+=gridSize;
            activePiece.y++;
            lastTic=0;
        }
    }
    
    if(!DEBUG && lastTic>=1){
        if(!step()){
            fix();
            spawn();
        }
        lastTic=0;
    }
}