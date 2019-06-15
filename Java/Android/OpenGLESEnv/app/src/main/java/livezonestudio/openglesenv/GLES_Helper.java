package livezonestudio.openglesenv;

import android.opengl.GLES32;
import android.util.Log;

public class GLES_Helper {
    static int checkForGLES32_errors(String tag, String message)
    {
        int error;
        while ((error = GLES32.glGetError()) != GLES32.GL_NO_ERROR) {
            Log.e(tag, message + " : " + error);
        }

        return 0;
    }
}
