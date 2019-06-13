package livezonestudio.openglesenv;

import android.content.Context;
import android.opengl.GLES32;
import android.opengl.GLSurfaceView;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;

import javax.microedition.khronos.egl.EGLConfig;
import javax.microedition.khronos.opengles.GL10;

public class MainActivity extends AppCompatActivity {
    private GLSurfaceView oglsurface;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        oglsurface = new CustomOpenGLSurfaceView(this);
        setContentView(oglsurface);
    }

    private class CustomOpenGLSurfaceView extends GLSurfaceView
    {
        private CustomOpenGLRenderer renderer;

        public CustomOpenGLSurfaceView(Context context) {
            super(context);

            setEGLContextClientVersion(3);

            renderer = new CustomOpenGLRenderer();

            setRenderer(renderer);
            setRenderMode(RENDERMODE_WHEN_DIRTY);
        }
    }

    private class CustomOpenGLRenderer implements GLSurfaceView.Renderer
    {

        @Override
        public void onSurfaceCreated(GL10 gl10, EGLConfig eglConfig) {
            GLES32.glClearColor(0.f, 1.f, 0.4f, 1.f);
        }

        @Override
        public void onSurfaceChanged(GL10 gl10, int width, int height) {
            GLES32.glViewport(0, 0, width, height);
        }

        @Override
        public void onDrawFrame(GL10 gl10) {
            GLES32.glClear(GLES32.GL_COLOR_BUFFER_BIT);

        }
    }
}
