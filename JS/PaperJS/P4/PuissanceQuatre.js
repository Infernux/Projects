var size = 800;
var width = 60;
var offset = 5;
var last = 0;
var gridCanvas;

var hauteur = 8, largeur = 8;

var player = 1;

//initialisation de la grille
var grid = [];
for(var i=0; i<largeur; i++){
    var column = [];
    for(var j=0; j<hauteur; j++){
        column.push(0);
    }
    grid.push(column);
}

var bg = Path.Rectangle(new Point(0,0), new Size(size,size));
bg.fillColor = 'black'

gridCanvas = initGridCanvas(); //création des Path

function initGridCanvas(){
    var res = [];
    for(var i=0; i<largeur; ++i){
        var resC = [];
        for(var j=0;j<hauteur; ++j){
            var shape = Path.Rectangle(new Point((width+offset)*i,(width+offset)*j),
                new Size(width,width));
            shape.fillColor = 'grey';
            resC.push(shape);
        }
        res.push(resC);
    }
    return res;
}

function drawGrid(){
    for(var i=0; i<largeur; ++i){
        for(var j=0;j<hauteur; ++j){
            if(grid[i][j]===1)
                gridCanvas[i][j].fillColor = 'red'
            if(grid[i][j]===2)
                gridCanvas[i][j].fillColor = 'yellow'
        }
    }
}

//compte le nombre de pions dans une colonne
function columnNumber(col){
    var count = 0;
    for(var i=0; i<hauteur; i++)
        if(grid[col][i]!==0)
            count++;
    return count;
}

function putPiece(col, player){
    var i;
    if(columnNumber(col)===hauteur)
        return -1;
        
    for(i=0; i<hauteur; i++){
        if(grid[col][i]!==0){
            grid[col][i-1]=player;
            return i-1;
        }
    }
    grid[col][i-1]=player;
    return i-1;
}

function nextTurn(){
    player = player===1?2:1;
}

function onMouseDown(event) {
    var col = event.point.x/((width+offset)*largeur)*largeur;
	col = Math.floor(col);
	col = col>=largeur?largeur-1:col;
	
	var y = putPiece(col,player);
	if(y!=-1){
        console.log(isWinning(col,y));
        nextTurn();
	}
}

function isWinning(x,y){
    //horizontal
    var count = 1;
    if(x-1>=0)
        count+=checkDirection(player,x-1,y,-1,0);
    if(x+1<largeur-1)
        count+=checkDirection(player,x+1,y,1,0);
        
    if(count>=4)return true;
    
    //diag up-left/down-right
    count = 1;
    if(x-1>=0 && y-1>=0)
        count+=checkDirection(player,x-1,y-1,-1,-1);
    if(x+1<largeur-1 && y+1<hauteur-1)
        count+=checkDirection(player,x+1,y+1,1,1);
    if(count>=4)return true;
    
    //vertical
    count = 1;
    if(y-1>=0)
        count+=checkDirection(player,x,y-1,0,-1);
    if(y+1<hauteur-1)
        count+=checkDirection(player,x,y+1,0,1);
    if(count>=4)return true;
    
    //diag down-left/up-right
    count = 1;
    if(x-1>=0 && y+1<largeur-1)
        count+=checkDirection(player,x-1,y+1,-1,1);
    if(x+1<largeur-1 && y-1<=0)
        count+=checkDirection(player,x+1,y-1,1,-1);
    if(count>=4)return true;
    return false;
}

//fait une verification récursive dans une direction
function checkDirection(player,x,y,dx,dy){
    return grid[x][y]===player?
        (((x+dx>=0 && x+dx<largeur)&&(y+dy>=0 && y+dy<largeur)))?
        1+checkDirection(player,x+dx,y+dy,dx,dy):1:0;
}

function onFrame(event) {
    last+=event.delta;
    
    if(last<0.1)
        return
    last=0;
    
    drawGrid();
}