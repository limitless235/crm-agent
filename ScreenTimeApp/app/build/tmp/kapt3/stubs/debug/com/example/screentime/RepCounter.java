package com.example.screentime;

import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;
import com.google.mediapipe.tasks.vision.poselandmarker.PoseLandmarkerResult;

@kotlin.Metadata(mv = {1, 9, 0}, k = 1, xi = 48, d1 = {"\u00008\n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0002\u0010\b\n\u0000\n\u0002\u0010\u000b\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0003\n\u0002\u0010\u0007\n\u0000\n\u0002\u0010\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0002\u0018\u00002\u00020\u0001B\u0005\u00a2\u0006\u0002\u0010\u0002J\u000e\u0010\u000e\u001a\u00020\u000f2\u0006\u0010\u0010\u001a\u00020\u0011J\u0006\u0010\u0012\u001a\u00020\u000fR\u0014\u0010\u0003\u001a\b\u0012\u0004\u0012\u00020\u00050\u0004X\u0082\u0004\u00a2\u0006\u0002\n\u0000R\u000e\u0010\u0006\u001a\u00020\u0007X\u0082\u000e\u00a2\u0006\u0002\n\u0000R\u0017\u0010\b\u001a\b\u0012\u0004\u0012\u00020\u00050\t\u00a2\u0006\b\n\u0000\u001a\u0004\b\n\u0010\u000bR\u000e\u0010\f\u001a\u00020\rX\u0082D\u00a2\u0006\u0002\n\u0000\u00a8\u0006\u0013"}, d2 = {"Lcom/example/screentime/RepCounter;", "", "()V", "_repCount", "Landroidx/lifecycle/MutableLiveData;", "", "isDown", "", "repCount", "Landroidx/lifecycle/LiveData;", "getRepCount", "()Landroidx/lifecycle/LiveData;", "threshold", "", "processResult", "", "result", "Lcom/google/mediapipe/tasks/vision/poselandmarker/PoseLandmarkerResult;", "reset", "app_debug"})
public final class RepCounter {
    @org.jetbrains.annotations.NotNull
    private final androidx.lifecycle.MutableLiveData<java.lang.Integer> _repCount = null;
    @org.jetbrains.annotations.NotNull
    private final androidx.lifecycle.LiveData<java.lang.Integer> repCount = null;
    private boolean isDown = false;
    private final float threshold = 0.05F;
    
    public RepCounter() {
        super();
    }
    
    @org.jetbrains.annotations.NotNull
    public final androidx.lifecycle.LiveData<java.lang.Integer> getRepCount() {
        return null;
    }
    
    public final void processResult(@org.jetbrains.annotations.NotNull
    com.google.mediapipe.tasks.vision.poselandmarker.PoseLandmarkerResult result) {
    }
    
    public final void reset() {
    }
}