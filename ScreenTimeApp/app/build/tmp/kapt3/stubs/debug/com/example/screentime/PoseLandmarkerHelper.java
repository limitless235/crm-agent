package com.example.screentime;

import android.content.Context;
import android.os.SystemClock;
import android.util.Log;
import com.google.mediapipe.framework.image.MPImage;
import com.google.mediapipe.tasks.core.BaseOptions;
import com.google.mediapipe.tasks.core.Delegate;
import com.google.mediapipe.tasks.vision.core.RunningMode;
import com.google.mediapipe.tasks.vision.poselandmarker.PoseLandmarker;
import com.google.mediapipe.tasks.vision.poselandmarker.PoseLandmarkerResult;

@kotlin.Metadata(mv = {1, 9, 0}, k = 1, xi = 48, d1 = {"\u0000@\n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0006\n\u0002\u0018\u0002\n\u0000\n\u0002\u0010\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0002\b\u0004\u0018\u00002\u00020\u0001:\u0001\u001aB\u0015\u0012\u0006\u0010\u0002\u001a\u00020\u0003\u0012\u0006\u0010\u0004\u001a\u00020\u0005\u00a2\u0006\u0002\u0010\u0006J\u000e\u0010\r\u001a\u00020\u000e2\u0006\u0010\u000f\u001a\u00020\u0010J\u0014\u0010\u0011\u001a\u00020\u000e2\n\u0010\u0012\u001a\u00060\u0013j\u0002`\u0014H\u0002J\u0018\u0010\u0015\u001a\u00020\u000e2\u0006\u0010\u0016\u001a\u00020\u00172\u0006\u0010\u0018\u001a\u00020\u0010H\u0002J\b\u0010\u0019\u001a\u00020\u000eH\u0002R\u0011\u0010\u0002\u001a\u00020\u0003\u00a2\u0006\b\n\u0000\u001a\u0004\b\u0007\u0010\bR\u0011\u0010\u0004\u001a\u00020\u0005\u00a2\u0006\b\n\u0000\u001a\u0004\b\t\u0010\nR\u0010\u0010\u000b\u001a\u0004\u0018\u00010\fX\u0082\u000e\u00a2\u0006\u0002\n\u0000\u00a8\u0006\u001b"}, d2 = {"Lcom/example/screentime/PoseLandmarkerHelper;", "", "context", "Landroid/content/Context;", "listener", "Lcom/example/screentime/PoseLandmarkerHelper$LandmarkerListener;", "(Landroid/content/Context;Lcom/example/screentime/PoseLandmarkerHelper$LandmarkerListener;)V", "getContext", "()Landroid/content/Context;", "getListener", "()Lcom/example/screentime/PoseLandmarkerHelper$LandmarkerListener;", "poseLandmarker", "Lcom/google/mediapipe/tasks/vision/poselandmarker/PoseLandmarker;", "detectLiveStream", "", "image", "Lcom/google/mediapipe/framework/image/MPImage;", "returnLivestreamError", "error", "Ljava/lang/RuntimeException;", "Lkotlin/RuntimeException;", "returnLivestreamResult", "result", "Lcom/google/mediapipe/tasks/vision/poselandmarker/PoseLandmarkerResult;", "input", "setupPoseLandmarker", "LandmarkerListener", "app_debug"})
public final class PoseLandmarkerHelper {
    @org.jetbrains.annotations.NotNull
    private final android.content.Context context = null;
    @org.jetbrains.annotations.NotNull
    private final com.example.screentime.PoseLandmarkerHelper.LandmarkerListener listener = null;
    @org.jetbrains.annotations.Nullable
    private com.google.mediapipe.tasks.vision.poselandmarker.PoseLandmarker poseLandmarker;
    
    public PoseLandmarkerHelper(@org.jetbrains.annotations.NotNull
    android.content.Context context, @org.jetbrains.annotations.NotNull
    com.example.screentime.PoseLandmarkerHelper.LandmarkerListener listener) {
        super();
    }
    
    @org.jetbrains.annotations.NotNull
    public final android.content.Context getContext() {
        return null;
    }
    
    @org.jetbrains.annotations.NotNull
    public final com.example.screentime.PoseLandmarkerHelper.LandmarkerListener getListener() {
        return null;
    }
    
    private final void setupPoseLandmarker() {
    }
    
    public final void detectLiveStream(@org.jetbrains.annotations.NotNull
    com.google.mediapipe.framework.image.MPImage image) {
    }
    
    private final void returnLivestreamResult(com.google.mediapipe.tasks.vision.poselandmarker.PoseLandmarkerResult result, com.google.mediapipe.framework.image.MPImage input) {
    }
    
    private final void returnLivestreamError(java.lang.RuntimeException error) {
    }
    
    @kotlin.Metadata(mv = {1, 9, 0}, k = 1, xi = 48, d1 = {"\u0000\u001e\n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0000\n\u0002\u0010\u0002\n\u0000\n\u0002\u0010\u000e\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0000\bf\u0018\u00002\u00020\u0001J\u0010\u0010\u0002\u001a\u00020\u00032\u0006\u0010\u0004\u001a\u00020\u0005H&J\u0010\u0010\u0006\u001a\u00020\u00032\u0006\u0010\u0007\u001a\u00020\bH&\u00a8\u0006\t"}, d2 = {"Lcom/example/screentime/PoseLandmarkerHelper$LandmarkerListener;", "", "onError", "", "error", "", "onResults", "result", "Lcom/google/mediapipe/tasks/vision/poselandmarker/PoseLandmarkerResult;", "app_debug"})
    public static abstract interface LandmarkerListener {
        
        public abstract void onError(@org.jetbrains.annotations.NotNull
        java.lang.String error);
        
        public abstract void onResults(@org.jetbrains.annotations.NotNull
        com.google.mediapipe.tasks.vision.poselandmarker.PoseLandmarkerResult result);
    }
}