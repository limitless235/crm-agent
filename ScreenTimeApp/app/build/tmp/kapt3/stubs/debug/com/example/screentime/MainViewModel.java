package com.example.screentime;

import android.os.Bundle;
import androidx.activity.ComponentActivity;
import androidx.compose.foundation.layout.*;
import androidx.compose.material3.*;
import androidx.compose.runtime.*;
import androidx.compose.runtime.State;
import androidx.compose.ui.Alignment;
import androidx.compose.ui.Modifier;
import android.content.Intent;
import android.net.Uri;
import android.os.PowerManager;
import android.provider.Settings;
import androidx.activity.result.contract.ActivityResultContracts;
import android.Manifest;
import android.content.pm.PackageManager;
import androidx.core.content.ContextCompat;
import com.example.screentime.db.AppDatabase;
import kotlinx.coroutines.Dispatchers;
import androidx.lifecycle.ViewModel;
import androidx.camera.view.PreviewView;
import com.example.screentime.PoseLandmarkerHelper;
import com.google.mediapipe.tasks.vision.poselandmarker.PoseLandmarkerResult;
import com.google.mediapipe.framework.image.BitmapImageBuilder;
import com.google.mediapipe.framework.image.MPImage;
import android.graphics.Bitmap;
import androidx.camera.core.*;
import androidx.camera.lifecycle.ProcessCameraProvider;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import android.util.Log;
import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;
import android.content.Context;
import android.content.pm.ApplicationInfo;
import android.graphics.drawable.Drawable;
import com.example.screentime.ExerciseCredit;

@kotlin.Metadata(mv = {1, 9, 0}, k = 1, xi = 48, d1 = {"\u0000p\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0002\u0010 \n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\u0010\u000e\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0003\n\u0002\u0010\b\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0005\n\u0002\u0018\u0002\n\u0002\b\u000b\n\u0002\u0010\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0002\b\u0004\n\u0002\u0010\t\n\u0000\u0018\u00002\u00020\u0001B\u0015\u0012\u0006\u0010\u0002\u001a\u00020\u0003\u0012\u0006\u0010\u0004\u001a\u00020\u0005\u00a2\u0006\u0002\u0010\u0006J\u000e\u0010(\u001a\u00020)2\u0006\u0010*\u001a\u00020+J\u000e\u0010,\u001a\u00020)2\u0006\u0010-\u001a\u00020.J\u000e\u0010/\u001a\u00020)2\u0006\u00100\u001a\u00020\u0015J\u000e\u00101\u001a\u00020)2\u0006\u00102\u001a\u000203R\u001a\u0010\u0007\u001a\u000e\u0012\n\u0012\b\u0012\u0004\u0012\u00020\n0\t0\bX\u0082\u0004\u00a2\u0006\u0002\n\u0000R\u0014\u0010\u000b\u001a\b\u0012\u0004\u0012\u00020\r0\fX\u0082\u0004\u00a2\u0006\u0002\n\u0000R\u000e\u0010\u0004\u001a\u00020\u0005X\u0082\u0004\u00a2\u0006\u0002\n\u0000R\u000e\u0010\u000e\u001a\u00020\u000fX\u0082\u0004\u00a2\u0006\u0002\n\u0000R\u000e\u0010\u0002\u001a\u00020\u0003X\u0082\u0004\u00a2\u0006\u0002\n\u0000R\u001d\u0010\u0010\u001a\u000e\u0012\n\u0012\b\u0012\u0004\u0012\u00020\n0\t0\u0011\u00a2\u0006\b\n\u0000\u001a\u0004\b\u0012\u0010\u0013R\u000e\u0010\u0014\u001a\u00020\u0015X\u0082\u000e\u00a2\u0006\u0002\n\u0000R\u0017\u0010\u0016\u001a\b\u0012\u0004\u0012\u00020\r0\u0017\u00a2\u0006\b\n\u0000\u001a\u0004\b\u0018\u0010\u0019R\u0017\u0010\u001a\u001a\b\u0012\u0004\u0012\u00020\u00150\u0017\u00a2\u0006\b\n\u0000\u001a\u0004\b\u001b\u0010\u0019R\u0011\u0010\u001c\u001a\u00020\u001d\u00a2\u0006\b\n\u0000\u001a\u0004\b\u001e\u0010\u001fR+\u0010!\u001a\u00020\r2\u0006\u0010 \u001a\u00020\r8F@FX\u0086\u008e\u0002\u00a2\u0006\u0012\n\u0004\b&\u0010\'\u001a\u0004\b\"\u0010#\"\u0004\b$\u0010%\u00a8\u00064"}, d2 = {"Lcom/example/screentime/MainViewModel;", "Landroidx/lifecycle/ViewModel;", "creditDao", "Lcom/example/screentime/db/ExerciseCreditDao;", "blockedDao", "Lcom/example/screentime/db/BlockedAppDao;", "(Lcom/example/screentime/db/ExerciseCreditDao;Lcom/example/screentime/db/BlockedAppDao;)V", "_installedApps", "Landroidx/compose/runtime/MutableState;", "", "Lcom/example/screentime/AppInfo;", "_motivationalText", "Landroidx/lifecycle/MutableLiveData;", "", "coachEngine", "Lcom/example/screentime/SmartCoachEngine;", "installedApps", "Landroidx/compose/runtime/State;", "getInstalledApps", "()Landroidx/compose/runtime/State;", "lastRepCount", "", "motivationalText", "Landroidx/lifecycle/LiveData;", "getMotivationalText", "()Landroidx/lifecycle/LiveData;", "repCount", "getRepCount", "repCounter", "Lcom/example/screentime/RepCounter;", "getRepCounter", "()Lcom/example/screentime/RepCounter;", "<set-?>", "targetApp", "getTargetApp", "()Ljava/lang/String;", "setTargetApp", "(Ljava/lang/String;)V", "targetApp$delegate", "Landroidx/compose/runtime/MutableState;", "fetchInstalledApps", "", "context", "Landroid/content/Context;", "processPoseResult", "result", "Lcom/google/mediapipe/tasks/vision/poselandmarker/PoseLandmarkerResult;", "syncRepsWithDb", "currentReps", "updateMotivationalMessage", "creditsInSeconds", "", "app_debug"})
public final class MainViewModel extends androidx.lifecycle.ViewModel {
    @org.jetbrains.annotations.NotNull
    private final com.example.screentime.db.ExerciseCreditDao creditDao = null;
    @org.jetbrains.annotations.NotNull
    private final com.example.screentime.db.BlockedAppDao blockedDao = null;
    @org.jetbrains.annotations.NotNull
    private final com.example.screentime.RepCounter repCounter = null;
    @org.jetbrains.annotations.NotNull
    private final androidx.lifecycle.LiveData<java.lang.Integer> repCount = null;
    @org.jetbrains.annotations.NotNull
    private final com.example.screentime.SmartCoachEngine coachEngine = null;
    @org.jetbrains.annotations.NotNull
    private final androidx.lifecycle.MutableLiveData<java.lang.String> _motivationalText = null;
    @org.jetbrains.annotations.NotNull
    private final androidx.lifecycle.LiveData<java.lang.String> motivationalText = null;
    @org.jetbrains.annotations.NotNull
    private final androidx.compose.runtime.MutableState targetApp$delegate = null;
    @org.jetbrains.annotations.NotNull
    private final androidx.compose.runtime.MutableState<java.util.List<com.example.screentime.AppInfo>> _installedApps = null;
    @org.jetbrains.annotations.NotNull
    private final androidx.compose.runtime.State<java.util.List<com.example.screentime.AppInfo>> installedApps = null;
    private int lastRepCount = 0;
    
    public MainViewModel(@org.jetbrains.annotations.NotNull
    com.example.screentime.db.ExerciseCreditDao creditDao, @org.jetbrains.annotations.NotNull
    com.example.screentime.db.BlockedAppDao blockedDao) {
        super();
    }
    
    @org.jetbrains.annotations.NotNull
    public final com.example.screentime.RepCounter getRepCounter() {
        return null;
    }
    
    @org.jetbrains.annotations.NotNull
    public final androidx.lifecycle.LiveData<java.lang.Integer> getRepCount() {
        return null;
    }
    
    @org.jetbrains.annotations.NotNull
    public final androidx.lifecycle.LiveData<java.lang.String> getMotivationalText() {
        return null;
    }
    
    @org.jetbrains.annotations.NotNull
    public final java.lang.String getTargetApp() {
        return null;
    }
    
    public final void setTargetApp(@org.jetbrains.annotations.NotNull
    java.lang.String p0) {
    }
    
    @org.jetbrains.annotations.NotNull
    public final androidx.compose.runtime.State<java.util.List<com.example.screentime.AppInfo>> getInstalledApps() {
        return null;
    }
    
    public final void syncRepsWithDb(int currentReps) {
    }
    
    public final void fetchInstalledApps(@org.jetbrains.annotations.NotNull
    android.content.Context context) {
    }
    
    public final void processPoseResult(@org.jetbrains.annotations.NotNull
    com.google.mediapipe.tasks.vision.poselandmarker.PoseLandmarkerResult result) {
    }
    
    public final void updateMotivationalMessage(long creditsInSeconds) {
    }
}