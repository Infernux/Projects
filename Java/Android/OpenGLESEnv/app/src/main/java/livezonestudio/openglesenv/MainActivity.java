package livezonestudio.openglesenv;

import android.content.Context;
import android.opengl.GLES20;
import android.opengl.GLES32;
import android.opengl.GLSurfaceView;
import android.opengl.Matrix;
import android.support.v4.content.res.ResourcesCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;

import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.nio.FloatBuffer;

import javax.microedition.khronos.egl.EGLConfig;
import javax.microedition.khronos.opengles.GL10;

import static android.opengl.GLSurfaceView.RENDERMODE_WHEN_DIRTY;

public class MainActivity extends AppCompatActivity {
    private GLSurfaceView oglsurface;
    private String TAG = "gles";

    private CustomOpenGLRenderer renderer;
    int vPosition;
    int uMVPMatrix;
    private float[] viewMatrix = new float[16];
    private float[] mvpMatrix = new float[16];
    private float[] projectionMatrix = new float[16];
    private float[] rotationMatrix = new float[16];
    private float scale = 1;

    private static String POSITION = "vposition";
    private static String MVP_MATRIX = "mvpmatrix";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        oglsurface = new CustomOpenGLSurfaceView(this);
        oglsurface.setEGLContextClientVersion(3);
        renderer = new CustomOpenGLRenderer();

        oglsurface.setRenderer(renderer);
        oglsurface.setRenderMode(RENDERMODE_WHEN_DIRTY);

        setContentView(oglsurface);
    }



    private static final String myShader =
            "varying vec2 position;" +
             "precision mediump float;" +
            "#define mode 0" +
"#define nbPoints 6" +
"void main()" +
"{" +
    "vec2 seeds[nbPoints];" +
    "seeds[0]=vec2(360.0, 23.2);" +
    "seeds[1]=vec2(80.0, 65.2);" +
    "seeds[2]=vec2(520.0, 280.2);" +
    "seeds[3]=vec2(42.0, 320.2);" +
    "seeds[4]=vec2(420.0, 160.2);" +
    "seeds[5]=vec2(300.0+sin(iTime)*50.0, 150.0+cos(iTime)*100.0);" +
    "int closest=0;" +
    "float closestV=1000.0;" +
    "for(int i=0; i<nbPoints; ++i){" +
        "float d1=pow(position.x-seeds[i].x,2.0);" +
        "float d2=pow(position.y-seeds[i].y,2.0);" +
        "float dist=sqrt(d1+d2);" +
        "if(dist<closestV){" +
        	"closestV=dist;" +
            "closest=i;" +
        "}" +
    "}" +
    "if(mode==1)" +
    	"closestV=closestV/100.0;" +
    "if(mode==0){" +
        "if(closest==0)" +
            "gl_FragColor=vec4(1.0,1.0,1.0,1.0);" +
        "else if(closest==1)" +
            "gl_FragColor=vec4(1.0,1.0,0.0,1.0);" +
        "else if(closest==2)" +
            "gl_FragColor=vec4(1.0,0.0,1.0,1.0);" +
        "else if(closest==3)" +
            "gl_FragColor=vec4(0.0,1.0,1.0,1.0);" +
        "else if(closest==4)" +
            "gl_FragColor=vec4(0.0,0.0,1.0,1.0);" +
        "else" +
            "gl_FragColor=vec4(0.0,0.0,0.0,0.0);" +
    "}" +
    "if(mode==1)" +
    	"gl_FragColor=vec4(closestV,1.0-closestV,0.0,1.0);" +
    "vec2 uv = position.xy / iResolution.xy;" +
    "for(int i=0; i<nbPoints; ++i){" +
        "if(position.x>=seeds[i].x-10.0 && position.x<=seeds[i].x+10.0 &&" +
           "position.y>=seeds[i].y-10.0 && position.y<=seeds[i].y+10.0){" +
            "//gl_FragColor=vec4(uv,0.5+0.5*sin(iTime),1.0);" +
            "gl_FragColor=vec4(1.0,0.0,0.0,1.0);" +
            "break;" +
        "}" +
    "}" +
"}";
        private static final String vertexshader = "" +
            "precision mediump float;" +
"uniform mat4 mvpmatrix;" +
"attribute vec4 " + POSITION +";" +
"varying vec2 position;" +
"void main() {" +
  "gl_Position = mvpmatrix * " + POSITION + ";" +
            "position = gl_Position.xy;" +
"}";

    private String fragmentShader = "precision mediump float;" +
"varying vec2 position;" +
"void main() {" +
  "gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);" +
"}";

    private int program;
    int position_location;

    private class CustomOpenGLSurfaceView extends GLSurfaceView
    {
        public CustomOpenGLSurfaceView(Context context) {
            super(context);
        }
    }

    private static final float[] POSITION_MATRIX = {
            -1,-1, 1,  // X1,Y1,Z1
            1,-1, 1,  // X2,Y2,Z2
            -1, 1, 1,  // X3,Y3,Z3
            1, 1, 1,  // X4,Y4,Z4
    };
    private FloatBuffer positionBuffer = ByteBuffer.allocateDirect(POSITION_MATRIX.length * 4)
            .order(ByteOrder.nativeOrder()).asFloatBuffer().put(POSITION_MATRIX);

    private class CustomOpenGLRenderer implements GLSurfaceView.Renderer
    {
        private int width, height;
        public int loadShader(int type, String shader)
        {
            int[] compiled = new int[1];
            //type is either VERTEX or FRAGMENT_SHADER
            int shader_id = GLES32.glCreateShader(type);

            GLES32.glShaderSource(shader_id, shader);
            GLES32.glCompileShader(shader_id);

            GLES32.glGetShaderiv(shader_id, GLES32.GL_COMPILE_STATUS, compiled, 0);
            if (compiled[0] == 0) {
                throw new RuntimeException("Compilation failed : " + GLES32.glGetShaderInfoLog(shader_id));
            }

            return shader_id;
        }

        @Override
        public void onSurfaceCreated(GL10 gl10, EGLConfig eglConfig) {
            GLES32.glClearColor(0f, 0f, 0f, 0f);
            Matrix.setRotateM(rotationMatrix, 0, 0, 0, 0, 1.0f);

            int []link = new int[1];
            int vertex_shader_id = loadShader(GLES32.GL_VERTEX_SHADER, vertexshader);
            int fragment_shader_id = loadShader(GLES32.GL_FRAGMENT_SHADER, fragmentShader);

            program = GLES32.glCreateProgram();

            GLES32.glAttachShader(program, vertex_shader_id);
            GLES32.glAttachShader(program, fragment_shader_id);
            GLES32.glLinkProgram(program);

            GLES_Helper.checkForGLES32_errors(TAG, "GLError");

            //position_location = GLES32.glGetAttribLocation(program, "position");
            GLES32.glGetProgramiv(program, GLES32.GL_LINK_STATUS, link, 0);

            if (link[0] <= 0) {
                throw new RuntimeException("Program couldn't be loaded");
            }
            GLES32.glUseProgram(program);

            vPosition = GLES32.glGetAttribLocation(program, POSITION);
            uMVPMatrix = GLES32.glGetUniformLocation(program, MVP_MATRIX);
        }

        @Override
        public void onSurfaceChanged(GL10 gl10, int width, int height) {
            this.width = width;
            this.height = height;
            GLES32.glViewport(0, 0, width, height);

            float ratio = (float) width / height;
            Matrix.frustumM(projectionMatrix, 0, -ratio, ratio, -1, 1, 3, 7);

            oglsurface.requestRender();
        }

        @Override
        public void onDrawFrame(GL10 gl10) {
            GLES32.glClear(GLES32.GL_COLOR_BUFFER_BIT | GLES32.GL_DEPTH_BUFFER_BIT);

            // Using matrices, we set the camera at the center, advanced of 7 looking to the center back
            // of -1
            Matrix.setLookAtM(viewMatrix, 0, 0, 0, 7, 0, 0, -1, 0, 1, 0);
            // We combine the scene setup we have done in onSurfaceChanged with the camera setup
            Matrix.multiplyMM(mvpMatrix, 0, projectionMatrix, 0, viewMatrix, 0);
            // We combile that with the applied rotation
            Matrix.multiplyMM(mvpMatrix, 0, mvpMatrix, 0, rotationMatrix, 0);
            // Finally, we apply the scale to our Matrix
            Matrix.scaleM(mvpMatrix, 0, scale, scale, scale);
            // We attach the float array containing our Matrix to the correct handle
            GLES32.glUniformMatrix4fv(uMVPMatrix, 1, false, mvpMatrix, 0);

            positionBuffer.position(0);
            GLES32.glVertexAttribPointer(vPosition, 3, GLES32.GL_FLOAT, false, 0, positionBuffer);
            GLES32.glEnableVertexAttribArray(vPosition);

            GLES32.glDrawArrays(GLES32.GL_TRIANGLE_STRIP, 0, 4);

            GLES32.glDisableVertexAttribArray(vPosition);

            //GLES32.glVertexAttribPointer(position_location, 2, GLES20.GL_FLOAT, false, 0, positionBuffer);

        }
    }
}
