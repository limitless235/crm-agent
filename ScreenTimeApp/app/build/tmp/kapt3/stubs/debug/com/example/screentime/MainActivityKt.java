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

@kotlin.Metadata(mv = {1, 9, 0}, k = 2, xi = 48, d1 = {"\u0000&\n\u0000\n\u0002\u0010\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\u001a\u001c\u0010\u0000\u001a\u00020\u00012\u0012\u0010\u0002\u001a\u000e\u0012\u0004\u0012\u00020\u0004\u0012\u0004\u0012\u00020\u00010\u0003H\u0007\u001a \u0010\u0005\u001a\u00020\u00012\u0006\u0010\u0006\u001a\u00020\u00072\u0006\u0010\b\u001a\u00020\t2\u0006\u0010\n\u001a\u00020\u000bH\u0007\u00a8\u0006\f"}, d2 = {"CameraPreview", "", "onResult", "Lkotlin/Function1;", "Lcom/google/mediapipe/tasks/vision/poselandmarker/PoseLandmarkerResult;", "MainScreen", "dao", "Lcom/example/screentime/db/ExerciseCreditDao;", "blockedDao", "Lcom/example/screentime/db/BlockedAppDao;", "mainViewModel", "Lcom/example/screentime/MainViewModel;", "app_debug"})
public final class MainActivityKt {
    
    @androidx.compose.runtime.Composable
    public static final void MainScreen(@org.jetbrains.annotations.NotNull
    com.example.screentime.db.ExerciseCreditDao dao, @org.jetbrains.annotations.NotNull
    com.example.screentime.db.BlockedAppDao blockedDao, @org.jetbrains.annotations.NotNull
    com.example.screentime.MainViewModel mainViewModel) {
    }
    
    @androidx.compose.runtime.Composable
    public static final void CameraPreview(@org.jetbrains.annotations.NotNull
    kotlin.jvm.functions.Function1<? super com.google.mediapipe.tasks.vision.poselandmarker.PoseLandmarkerResult, kotlin.Unit> onResult) {
    }
}